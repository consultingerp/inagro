# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_crop_activity(models.Model):
    _name = 'crop.activity'

    name = fields.Many2one('farmer.location.crops',string='Crop Code',domain="[('active','=',True)]",required=True)
    category_id = fields.Many2one('crop.category',string='Category',related="name.category_id",store=True)
    varieties_id = fields.Many2one('crop.varieties',string='Varieties',related="name.varieties_id",store=True)
    area_location_id = fields.Many2one('res.partner',string='Location Area',related="name.area_location_id",store=True)
    date = fields.Date(string='Date',required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,default=lambda *a: 'draft')

    line_ids = fields.One2many('crop.activity.line', 'line_id','Activity detail',readonly=False,copy=True,track_visibility='onchange')

    @api.multi
    def button_confirm(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def button_validate(self):
        return self.write({'state': 'done'})

    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def button_draft(self):
        return self.write({'state': 'draft'})


class inagro_crop_activity_line(models.Model):

    _name = 'crop.activity.line'
    _description = "Detail activity"

    name = fields.Many2one('crop.masteractivity','Activity', required=True)
    description = fields.Text(string='Description')
    line_id = fields.Many2one('crop.activity','Activity',ondelete='cascade', readonly=True)