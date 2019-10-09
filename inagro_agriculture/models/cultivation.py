# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import namedtuple
import json
import time
from datetime import date

from itertools import groupby
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter

from odoo.exceptions import UserError, AccessError




class inagro_agriculture_Picking_cultivation(models.Model):
    _inherit = "stock.picking"

    is_cultivation = fields.Boolean(
        string='Is Cultivation?',
        copy=True
    )

    is_harvest = fields.Boolean(
        string='Is Harvest?',
        copy=True
    )

    # crop_id = fields.Many2one(
    #     'farmer.location.crops',
    #     domain="[('active','=',True)]",
    #     string='Crop Code'
    # )

    # varieties_id = fields.Many2one(
    #     'crop.varieties',
    #     string='Varieties',
    #     # related="crop_id.varieties_id",
    #     readonly=True
    # )

    # category_id = fields.Many2one(
    #     'crop.category',
    #     string='Category',
    #     related="varieties_id.category_id",
    #     readonly=True
    # )

    # area_location_id = fields.Many2one(
    #     'res.partner',
    #     string='Location Area',
    #     # related="crop_id.area_location_id",
    #     # readonly=True
    # )

    @api.multi
    def action_confirm(self):

        # if self.is_cultivation == True:
        #     # print (self.crop_id)
        #     if len(self.crop_id) <= 0:
        #         raise UserError(_('Crop code can not be empty'))

        for order in self:
            if order.is_harvest == True:
                if order.picking_type_id.is_harvest == False:
                    raise UserError(_('Operation Type is not compatible'))

        for order in self:
            if order.is_cultivation == True:
                if order.picking_type_id.is_cultivation == False:
                    raise UserError(_('Operation Type is not compatible'))



        for order in self:
            if order.is_cultivation == True:
                for line in order.move_ids_without_package:
                    if len(line.varieties_id) <= 0 or len(line.area_location_id) <= 0:
                        raise UserError(_('Varieties or Location Area can not be empty'))

        for order in self:
            if order.is_harvest == True:
                for line in order.move_ids_without_package:
                    if len(line.crop_id) <= 0:
                        raise UserError(_('Crop Code can not be empty'))


        self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'draft' and not pl.move_ids)._generate_moves()
        # call `_action_confirm` on every draft move

        # if self.is_harvest == False and self.is_cultivation == False:
        self.mapped('move_lines')\
            .filtered(lambda move: move.state == 'draft')\
            ._action_confirm()

        # call `_action_assign` on every confirmed move which location_id bypasses the reservation
        self.filtered(lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production') and picking.state == 'confirmed')\
            .mapped('move_lines')._action_assign()
        return True


class inagro_agriculture_StockMove(models.Model):
    _inherit = "stock.move"

    crop_id = fields.Many2one(
        'farmer.location.crops',
        domain="[('active','=',True)]",
        string='Crop Code'
    )

    crop_varieties_id = fields.Many2one(
        'crop.varieties',
        string='Crop Varieties',
        related="crop_id.varieties_id"
    )

    crop_category_id = fields.Many2one(
        'crop.category',
        string='Crop Category',
        related="crop_id.category_id",
        readonly=True
    )

    crop_area_location_id = fields.Many2one(
        'res.partner',
        domain="[('is_location','=',True)]",
        string='Crop Location Area',
        related="crop_id.area_location_id",
        # readonly=True
    )

    varieties_id = fields.Many2one(
        'crop.varieties',
        string='Varieties'
    )

    area_location_id = fields.Many2one(
        'res.partner',
        domain="[('is_location','=',True)]",
        string='Location Area'
        # related="crop_id.area_location_id",
        # readonly=True
    )

    is_cultivation = fields.Boolean(
        related="picking_id.is_cultivation",
        string='Is Cultivation?',
        store=True
    )

    is_harvest = fields.Boolean(
        related="picking_id.is_harvest",
        string='Is Harvest?',
        store=True
    )

    def _action_confirm(self, merge=True, merge_into=False):

        print('move confirm2')
        """ Confirms stock move or put it in waiting if it's linked to another move.
        :param: merge: According to this boolean, a newly confirmed move will be merged
        in another move of the same picking sharing its characteristics.
        """
        move_create_proc = self.env['stock.move']
        move_to_confirm = self.env['stock.move']
        move_waiting = self.env['stock.move']

        to_assign = {}
        for move in self:
            # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
            if move.move_orig_ids:
                move_waiting |= move
            else:
                if move.procure_method == 'make_to_order':
                    move_create_proc |= move
                else:
                    move_to_confirm |= move
            if move._should_be_assigned():
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = self.env['stock.move']
                to_assign[key] |= move

        # create procurements for make to order moves
        for move in move_create_proc:
            values = move._prepare_procurement_values()
            origin = (move.group_id and move.group_id.name or (move.origin or move.picking_id.name or "/"))
            self.env['procurement.group'].run(move.product_id, move.product_uom_qty, move.product_uom, move.location_id, move.rule_id and move.rule_id.name or "/", origin,
                                              values)

        move_to_confirm.write({'state': 'confirmed'})
        (move_waiting | move_create_proc).write({'state': 'waiting'})

        # assign picking in batch for all confirmed move that share the same details
        for moves in to_assign.values():
            moves._assign_picking()
        self._push_apply()

        # jika merupakan proses cultivation atau harvest maka move jangan di merge
        for move_cek in self:
            if move_cek.is_cultivation == False and move_cek.is_harvest == False:
                if merge:
                    return self._merge_moves(merge_into=merge_into)
        return self



