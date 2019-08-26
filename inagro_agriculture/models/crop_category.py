# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_crop_category(models.Model):
    _name = 'crop.category'

    name = fields.Char(string="Name Category",required=True)