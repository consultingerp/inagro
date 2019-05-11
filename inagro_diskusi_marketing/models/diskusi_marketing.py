# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Room_marketing(models.Model):
    _name = 'room.marketing'

    name = fields.Char('Room Name', required=True)
    capacity = fields.Integer('Capacity', required=True)

    _sql_constraints = [('room_marketing_uniq', 'unique (name)', 'Name room must be unique!')]

class Diskusi_marketing(models.Model):
    _name = 'diskusi.marketing'
    _inherit = ['mail.thread']

    name = fields.Char('Name')
    tanggal = fields.Date('Date')
    # product_id = fields.Many2one('product.product', string='Product',required=False, store=True)