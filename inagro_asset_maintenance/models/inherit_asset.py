# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class inagro_asset_MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    is_asset = fields.Boolean(string="Is Asset?",default=False)

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

