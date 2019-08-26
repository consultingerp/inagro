# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_crop_varieties(models.Model):
    _name = 'crop.varieties'

    name = fields.Char(string="Name Varieties",required=True)
    category = fields.Many2one('crop.category',string="Category",required=True)