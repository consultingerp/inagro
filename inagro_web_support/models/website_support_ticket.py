# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from docutils.nodes import field

class DepartementSupport(models.Model):
    
    _name = 'department.support'
    _description = "Department Support"
    _rec_name = "name"
    
    name = fields.Many2one('hr.department', string = 'Department')
    
    
class inheritWebsiteSupportTicketCategory(models.Model):

    _inherit = "website.support.ticket.category"
    
    department_id = fields.Many2one('department.support', string ='Category Department')

class inherit_WebsiteSupportTicket(models.Model):
     
    _inherit = 'website.support.ticket'
     
    department_id = fields.Many2one('department.support', string ='Department', related="category_id.department_id", store=True)
    
    

    