# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inherit_FleetVehicleLogFuel(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'

    purchaser_id = fields.Many2one('res.partner', 'Purchaser', domain="[('customer','=',False)]")


class inherit_FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    purchaser_id = fields.Many2one('res.partner', 'Purchaser', domain="[('customer','=',False)]")