# -*- coding: utf-8 -*-

from odoo import api, fields, models  


class inherit_FarmerLocationCrops(models.Model):
	_inherit = 'farmer.location.crops'

	name = fields.Char(
		string='Code',
		required=True
	)

	crop_period_start = fields.Date(
		string='Crop Period Start',
		required=True
	)
	crop_period_end = fields.Date(
		string='Crop Period End',
		required=False
	)

	crop_type = fields.Selection(
		[('TBM','TBM'),
		('TM', 'TM')], 
		string='Crop Type', 
		default ='TBM',
		store = True
	)
        
	area_location_id = fields.Many2one(
		'res.partner',
		string='Location Area',
		domain="[('is_location','=',True)]",
		required=True
	)

	active = fields.Boolean(string="active", default=True)

	old_code_id = fields.Many2one(
		'farmer.location.crops',
		domain="[('active','=',False)]",
		string='Old Code'
	)

	category_id = fields.Many2one(
		'crop.category',
		string='Category',
		required=True
	)

	commodity_type = fields.Many2one('commodity.type',string="Commodity Type",related="category_id.commodity_type",store=True)

	activity_line = fields.Many2one('crop.activity.line', string='Activity Line')

	_sql_constraints = [
        ('name_unique', 'unique(name)', 'Code already exists!')
    ]

	@api.onchange('category_id')
	def _onchange_category(self):
		print('tes')
		domain = [('category', '=', self.category_id.id)]
		return {'domain': {'varieties_id': domain}}
		# for item in self:
		# 	item.varieties_id = self.env['crop.varieties'].search([('category', '=', item.category_id.id)])
	
	varieties_id = fields.Many2one(
		'crop.varieties',
		string='Varieties',
		required=True
	)

	warehouse_id = fields.Many2one(
		'stock.warehouse',
		string='Warehouse',
		required=False
	)
	location_id = fields.Many2one(
		'stock.location',
		string='Stock Location',
		required=False
	)

