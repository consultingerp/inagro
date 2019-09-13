# -*- coding: utf-8 -*-

from odoo import api, fields, models  


class inagro_agriculture_resPartner(models.Model):
	_inherit = "res.partner"

	farmer_location_id = fields.Many2one(
		'res.partner',
		string='Location Area',
		domain="[('is_location','=',True)]",
	)