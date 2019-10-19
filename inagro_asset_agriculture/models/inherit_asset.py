
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class inagro_agriculture_asset_FarmerLocationCrops(models.Model):
	_inherit = 'farmer.location.crops'
	is_asset = fields.Boolean(string="Is Asset?",default=False)

class inagro_agriculture_asset_AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    is_crop = fields.Boolean(string="Is Crop?",default=False)

    crop_id = fields.Many2one(
        'farmer.location.crops',
        domain="[('active','=',True),('is_asset','=',False)]",
        string='Crop Code'
    )

    crop_varieties_id = fields.Many2one(
        'crop.varieties',
        string='Crop Varieties',
        related="crop_id.varieties_id",
        store=True
    )

    crop_category_id = fields.Many2one(
        'crop.category',
        string='Crop Category',
        related="crop_id.category_id",
        store=True
    )

    crop_area_location_id = fields.Many2one(
        'res.partner',
        domain="[('is_location','=',True)]",
        string='Crop Location Area',
        related="crop_id.area_location_id",
        store=True
        # readonly=True
    )

    @api.onchange('crop_id')
    def onchange_crop_id(self):
    	# print(self.crop_id)
    	self.name = self.crop_id.name

    @api.multi
    def validate(self):
    	#tambahan baru
    	if self.is_crop == True:
    		if len(self.crop_id) <= 0:
    			raise ValidationError(_('Crop is not selected'))

    	# print(self.crop_id,' id')
    	crop = self.env['farmer.location.crops'].search([('id', '=', int(self.crop_id))])
    	# print(crop,' mm')
    	crop.write({'is_asset': True})
    	#tambahan baru end

    	self.write({'state': 'open'})
    	fields = [
    		'method',
    		'method_number',
    		'method_period',
    		'method_end',
    		'method_progress_factor',
    		'method_time',
    		'salvage_value',
    		'invoice_id',
    	]
    	ref_tracked_fields = self.env['account.asset.asset'].fields_get(fields)
    	for asset in self:
    		tracked_fields = ref_tracked_fields.copy()
    		if asset.method == 'linear':
    			del(tracked_fields['method_progress_factor'])
    		if asset.method_time != 'end':
    			del(tracked_fields['method_end'])
    		else:
    			del(tracked_fields['method_number'])
    		dummy, tracking_value_ids = asset._message_track(tracked_fields, dict.fromkeys(fields))
    		asset.message_post(subject=_('Asset created'), tracking_value_ids=tracking_value_ids)

    @api.multi
    def set_to_draft(self):
    	#tambahan baru
    	crop = self.env['farmer.location.crops'].search([('id', '=', int(self.crop_id))])
    	crop.write({'is_asset': False})
    	#tambahan baru end

    	self.write({'state': 'draft'})




