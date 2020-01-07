# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime

class inherit_MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'
    
#     @api.model
#     def create(self, values):
#         values['sequence_char'] = self.env['ir.sequence'].next_by_code('increament_sequence') or _('New')
#         res = super(inherit_MrpProduction, self).create(values)
#         return res
#     
#     sequence_char = fields.Char('Sequence', readonly=True, track_visibility='onchange', 
#                             copy=False,index=True, store=True,
#                             default=lambda self: _('New'))
#     
    

class inherit_MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits=(16,3), required=True)
    
    
class inherit_MrpBom(models.Model):
    _inherit = 'mrp.bom'
    
    picking_id = fields.Many2one('stock.picking.type','Stock Operation', required=True)
    
    
class inherit_StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_uom_qty = fields.Float('Initial Demand',
        digits=(16,3), default=0.0, required=True, states={'done': [('readonly', True)]},
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")
    
    reserved_availability = fields.Float(
        'Quantity Reserved', compute='_compute_reserved_availability',
        digits=(16,3),
        readonly=True, help='Quantity that has already been reserved for this move')
    
    quantity_done = fields.Float('Quantity Done', compute='_quantity_done_compute', digits=(16,3), inverse='_quantity_done_set')
    