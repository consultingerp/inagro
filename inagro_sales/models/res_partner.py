# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.tools import pycompat
from docutils.nodes import Part
# from gevent.libev.corecext import self
# from odoo.addons.hw_screen.controllers.main import self_port


class inagro_Partner(models.Model):
    _inherit = "res.partner"
    
    

#     @api.onchange('company_type')
#     def onchange_company_type(self):
#         self.is_company = (self.company_type == 'company')
        
    @api.depends('is_company','is_school','is_community','is_person')
    def _compute_company_type(self):
        print("test")
        for partner in self:
            if partner.is_company:
                partner.company_type = 'company'
                 
            elif partner.is_school:
                partner.company_type = 'school'
                 
            elif partner.is_community:
                partner.company_type = 'community'
             
            elif partner.is_person :
                partner.company_type = 'person'
                 
            print(partner.company_type,' kkkk')
            
    def _write_company_type(self):
        print("tesht")
#         for partner in self:
#             if partner.is_company:
#                 partner.company_type = 'company'
#                 
#             elif partner.is_school:
#                 partner.company_type = 'school'
#                 
#             elif partner.is_community:
#                 partner.company_type = 'community'
#             
#             elif partner.is_person :
#                 partner.company_type = 'person'
# #             partner.is_company = partner.company_type == 'company'

    @api.onchange('company_type')
    def onchange_company_type(self):
        print ("tesst")
        for partner in self:
            if partner.company_type == 'company':
                return {'value':{'is_company' : True, 'is_school' : False, 'is_person' : False, 'is_community' : False}}
            elif partner.company_type == 'school':
                return {'value':{'is_company' : False, 'is_school' : True, 'is_person' : False, 'is_community' : False}}
            elif partner.company_type == 'person':
                return {'value':{'is_company' : False, 'is_school' : False, 'is_person' : True, 'is_community' : False}}
            elif partner.company_type == 'community':
                return {'value':{'is_company' : False, 'is_school' : False, 'is_person' : False, 'is_community' : True}}
            else:
                return {'value':{'is_company' : False, 'is_school' : False, 'is_person' : False, 'is_community' : False}}
             
            return True
                

    company_type = fields.Selection(string='Company Type',
        selection=[('person', 'Individual'), ('company', 'Company'),('school','School'),('community','Community')], compute='_compute_company_type')
    
    is_school = fields.Boolean(string='Is a School', default=False, store=True)
    is_person = fields.Boolean(string='Is a Individual', default=False, store=True)
    is_community = fields.Boolean(string='Is a Community', default=False, store=True)

        

    
    
    