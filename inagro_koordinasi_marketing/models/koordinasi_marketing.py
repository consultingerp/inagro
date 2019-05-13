# -*- coding: utf-8 -*-

from odoo import models, fields, api
_STATES = [
    ('draft', 'Draft'),
    ('confirm', 'Confirm'),
    ('cancel', 'Cancel')
]

# class Room_marketing(models.Model):
#     _name = 'room.marketing'

#     name = fields.Char('Room Name', required=True)
#     capacity = fields.Integer('Capacity', required=True)

#     _sql_constraints = [('room_marketing_uniq', 'unique (name)', 'Name room must be unique!')]

class outdoor_activities(models.Model):
    _name = 'ourdoor.activities'

    name = fields.Char('Name')
    _sql_constraints = [('activities_uniq', 'unique (name)', 'Name must be unique!')]

class facilities(models.Model):
    _name = 'facilities'

    name = fields.Char('Name')
    _sql_constraints = [('activities_uniq', 'unique (name)', 'Name must be unique!')]

# class food_beverage(models.Model):
#     _name = 'food.beverage'

#     name = fields.Char('Name')
#     _sql_constraints = [('food_uniq', 'unique (name)', 'Name must be unique!')]



class Koordinasi_marketing(models.Model):
    _name = 'koordinasi.marketing'
    _inherit = ['mail.thread']

    name = fields.Char('Activity Name',required=True)
    tanggal = fields.Date('Date')
    partner_id = fields.Many2one('res.partner', 'Customer',
                                 index=True,
                                 required=True)
    customer_pic = fields.Char('Customer PIC',required=True)
    customer_contact = fields.Char('Customer Contact',required=True)
    # employee_id = fields.Many2one('hr.employee', 'Emplopyee', readonly=True,
    #                              index=True,
    #                              required=True)
    date = fields.Date('Date',required=True)
    qty_participant = fields.Integer('Number of participants')
    qty_teacher = fields.Integer('Quantity Teacher')
    qty_add_participant = fields.Integer('Additional participants')
    total = fields.Integer('Total')

    state = fields.Selection(selection=_STATES,
                             string='State',
                             index=True,
                             required=True,
                             copy=False,
                             default='draft')
    # product_id = fields.Many2one('product.product', string='Product',required=False, store=True)


