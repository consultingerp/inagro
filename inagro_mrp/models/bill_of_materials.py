# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class inherit_MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'
    
#     location_id = fields.Many2one('stock.location', 'Location')