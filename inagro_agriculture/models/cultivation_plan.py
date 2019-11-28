# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.addons import decimal_precision as dp

class inagro_cultivation_plan(models.Model):
    _name = 'cultivation.plan'
    _inherit = ['mail.thread']

    name = fields.Selection([(num, str(num)) for num in range((datetime.now().year)-5 , (datetime.now().year)+5 )], 'Year')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,default=lambda *a: 'draft')
    line_ids = fields.One2many('cultivation.plan.line', 'line_id','Plan detail',readonly=False,copy=True,track_visibility='onchange')
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


class inagro_cultivation_plan_line(models.Model):

    _name = 'cultivation.plan.line'
    _description = "Detail cultivation plan"

    name = fields.Many2one('crop.varieties',string='Varieties',store=True)
    category = fields.Many2one('crop.category',string='Category',store=True,related="name.category")
    organic_date = fields.Many2many('cultivation.plan.line.date','cultivation_plan_line_organik_date_rel','organic_date',string='Organic Plan Date')
    an_organic_date = fields.Many2many('cultivation.plan.line.date','cultivation_plan_line_an_organik_date_rel','an_organic_date',string='An Organic Plan Date')
    line_id = fields.Many2one('cultivation.plan','Cultivation',ondelete='cascade', readonly=True)
    year = fields.Selection([(num, str(num)) for num in range(2010, (datetime.now().year)+5 )], 'Year',store=True,related="line_id.name")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True,store=True,related="line_id.state")

class inagro_cultivation_plan_line_date(models.Model):

    _name = 'cultivation.plan.line.date'
    _description = "Detail cultivation plan Date"

    name = fields.Date(string='Date',store=True)
    organic_date = fields.Many2one('cultivation.plan.line',string='Organic Plan Date')
    an_organic_date = fields.Many2one('cultivation.plan.line',string='An Organic Plan Date')