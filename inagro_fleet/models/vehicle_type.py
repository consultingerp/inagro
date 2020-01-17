# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inagro_fleet_vehicle_type(models.Model):
    _name = 'vehicle.type'

    name = fields.Char('Vehicle Type',required=True)


