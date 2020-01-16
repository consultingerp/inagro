from odoo import models, fields, api

class inagro_FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    state = fields.Selection([
        ('futur', 'Incoming'),
        ('open', 'In Progress'),
        ('diesoon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('closed', 'Closed')
        ], 'Status', default='futur', readonly=True,
        help='Choose whether the contract is still valid or not',
        track_visibility="onchange",
        copy=False)

    seats = fields.Integer('Seats Number of Vehicle',related="vehicle_id.seats", help='Number of seats vehicle')