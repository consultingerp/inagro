# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_crop_category(models.Model):
    _name = 'crop.category'

    name = fields.Char(string="Name Commodity",required=True)
    commodity_type = fields.Many2one('commodity.type',string="Commodity Type",required=True)