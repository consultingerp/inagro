# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_crop_masteractivity(models.Model):
    _name = 'crop.masteractivity'

    name = fields.Char(string="Name Activity",required=True)