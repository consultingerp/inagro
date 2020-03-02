

from odoo import api, fields, models, tools

class fleet_schedule(models.Model):
    _name = "fleet.schedule"
    _description = "Schedule"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    name = fields.Char('Name', readonly=True)
    start_date = fields.Date('Start Date')
    expiration_date = fields.Date('Expiration Date')
    state = fields.Selection([
        ('futur', 'Incoming'),
        ('sent', 'Sent to Progress'),
        ('open', 'In Progress'),
        ('expired', 'Expired'),
        ('cancel', 'Cancel'),
        ('closed', 'Closed')
        ], 'Status')
    vehicle_type = fields.Char('Type', readonly=True)
    passenger_ids = fields.One2many('vehicle.passenger', 'parent_id', 'Passenger', copy=False, readonly=True)


    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            )""" 
            % (self._table, self._select(), self._from(), self._group_by()))

    def _select(self):
        select_str = """
            SELECT
                min(A.id) as id,
                a . name,
                a .start_date,
                a .expiration_date,
                a .state,
                b. name AS vehicle_type,
                c. id as passenger_ids
        """
        return select_str

    def _from(self):
        from_str = """
                fleet_vehicle_log_contract a
                LEFT JOIN fleet_vehicle_state b ON a .vehicle_type_id = b. id
                LEFT JOIN vehicle_passenger c ON a.id = c.parent_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                a . name,
                a .start_date,
                a .expiration_date,
                a .state,
                b. name,
                c. id
        """
        return group_by_str



