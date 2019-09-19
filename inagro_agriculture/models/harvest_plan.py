# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.addons import decimal_precision as dp

class inagro_hasvest_plan(models.Model):
    _name = 'harvest.plan'
    _inherit = ['mail.thread']

    name = fields.Selection([(num, str(num)) for num in range(2010, (datetime.now().year)+5 )], 'Year')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,default=lambda *a: 'draft')
    line_ids = fields.One2many('harvest.plan.line', 'line_id','Plan detail',readonly=False,copy=True,track_visibility='onchange')
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Year already exists!')
    ]

    @api.multi
    def button_confirm(self):
        return self.write({'state': 'confirm'})

    @api.multi
    def button_validate(self):
        return self.write({'state': 'done'})

    # @api.multi
    # def button_cancel(self):
    #     return self.write({'state': 'cancel'})

    # @api.multi
    # def button_draft(self):
    #     return self.write({'state': 'draft'})


class inagro_hasvest_plan_line(models.Model):

    _name = 'harvest.plan.line'
    _description = "Detail harvest plan"

    name = fields.Many2one('crop.varieties',string='Varieties',store=True)
    product_id = fields.Many2one('product.product',string='Product',store=True)
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom',related="product_id.uom_id", string='Unit of Measure',store=True)
    # description = fields.Text(string='Description')
    line_id = fields.Many2one('harvest.plan','Harvest',ondelete='cascade', readonly=True)
    year = fields.Selection([(num, str(num)) for num in range(2010, (datetime.now().year)+5 )], 'Year',store=True,related="line_id.name")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,store=True,related="line_id.state")