# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class inagro_asset_MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    is_asset = fields.Boolean(string="Is Asset?",default=False)

    asset_id = fields.Many2one('account.asset.asset', string='Asset', domain=[('state', '=', 'open'),('is_equipment', '=', False)], store=True)

    @api.onchange('department_id')
    def onchange_department(self):
        asset_category = self.env['account.asset.category'].search([('department_id', '=', int(self.department_id))])
        domain_asset = [('category_id', '=',int(asset_category))]
        return {'domain': {'asset_id': domain_asset}}

    @api.onchange('asset_id')
    def onchange_asset_id(self):
        self.name = self.asset_id.name

        if len(self.asset_id) > 0:
            # print ('centang asset')
            self.is_asset = True
        else:
            self.is_asset = False

    @api.model
    def create(self, values):
        
        new_id = super(inagro_asset_MaintenanceEquipment, self).create(values)
        if values.get('asset_id'):
            
            asset = self.env['account.asset.asset'].search([('id', '=', int(values.get('asset_id')))])
            asset.write({'is_equipment': True,'equipment_id': int(new_id)})

        return new_id

class inagro_asset_AccountAssetCategory(models.Model):
    _inherit = 'account.asset.category'

    department_id = fields.Many2one('hr.department', string='Department', domain=[('active', '=', True)], store=True,)

class inagro_asset_AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    is_equipment = fields.Boolean(string="Is Equipment?",default=False)

    equipment_id = fields.Many2one(
        'maintenance.equipment',
        domain="[('active','=',True),('is_asset','=',False)]",
        string='Equipment'
    )

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
    	# print(self.crop_id)
    	self.name = self.equipment_id.serial_no

    # serial_no = fields.Char('SN Equipment', related="equipment_id.serial_no", store=True)

    @api.multi
    def validate(self):
        # print('tes data')\

        if self.is_equipment == True:
            if len(self.equipment_id) <= 0:
                raise ValidationError(_('Equipment is not selected'))

        # print(self.crop_id,' id')
        crop = self.env['maintenance.equipment'].search([('id', '=', int(self.equipment_id))])
        # print(crop,' mm')
        crop.write({'is_asset': True})
        #tambahan baru end

        result = super(inagro_asset_AccountAssetAsset, self).validate()    
        return result

