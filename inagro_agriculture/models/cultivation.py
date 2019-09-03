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

    crop_id = fields.Many2one(
        'farmer.location.crops',
        domain="[('active','=',True)]",
        string='Crop Code'
    )

    varieties_id = fields.Many2one(
        'crop.varieties',
        string='Varieties',
        related="crop_id.varieties_id",
        readonly=True
    )

    category_id = fields.Many2one(
        'crop.category',
        string='Category',
        related="crop_id.category_id",
        readonly=True
    )

    area_location_id = fields.Many2one(
        'res.partner',
        string='Location Area',
        related="crop_id.area_location_id",
        readonly=True
    )

    @api.multi
    def action_confirm(self):

        if self.is_cultivation == True:
            # print (self.crop_id)
            if len(self.crop_id) <= 0:
                raise UserError(_('Crop code can not be empty'))


        for order in self:
            if order.is_harvest == True:
                for line in order.move_ids_without_package:
                    if len(line.varieties_id) <= 0:
                        raise UserError(_('Varieties can not be empty'))



        self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'draft' and not pl.move_ids)._generate_moves()
        # call `_action_confirm` on every draft move
        self.mapped('move_lines')\
            .filtered(lambda move: move.state == 'draft')\
            ._action_confirm()
        # call `_action_assign` on every confirmed move which location_id bypasses the reservation
        self.filtered(lambda picking: picking.location_id.usage in ('supplier', 'inventory', 'production') and picking.state == 'confirmed')\
            .mapped('move_lines')._action_assign()
        return True


class inagro_agriculture_StockMove(models.Model):
    _inherit = "stock.move"

    varieties_id = fields.Many2one(
        'crop.varieties',
        string='Varieties'
    )



