# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from docutils.nodes import field

class DepartementSupport(models.Model):
    
    _name = 'department.support'
    _description = "Department Support"
    _rec_name = "name"
    
    name = fields.Many2one('hr.department', string = 'Department', store=True)
    
    
class inheritWebsiteSupportTicketCategory(models.Model):

    _inherit = "website.support.ticket.category"
    
    department_id = fields.Many2one('department.support', string ='Category Department')

class inherit_WebsiteSupportTicket(models.Model):
     
    _inherit = 'website.support.ticket'
     
    department_id = fields.Many2one('department.support', string ='Department', related="category_id.department_id", store=True)
    employee_id = fields.Many2one('hr.employee', string='User',store=True)
    dept_rel_id = fields.Many2one('hr.department', string='Department Related', related='department_id.name')
    closed_rel_id = fields.Many2one('hr.employee', string='Closed by Related')
    
    @api.onchange('employee_id')
    def onchange_user_id(self):
        if self.employee_id:
            self.user_id = self.employee_id.user_id
            
    @api.onchange('closed_rel_id')
    def onchange_closedby_id(self):
        if self.closed_rel_id:
            self.closed_by_id = self.closed_rel_id.user_id
    
    

    