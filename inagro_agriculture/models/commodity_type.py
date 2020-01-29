# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_commodity_type(models.Model):
    _name = 'commodity.type'

    name = fields.Char(string="Commodity Type",required=True)