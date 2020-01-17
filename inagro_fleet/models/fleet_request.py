# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Fleet_request(models.Model):
    _name = 'fleet.request'

    purchaser_id = fields.Many2one('res.partner', 'Purchaser')


