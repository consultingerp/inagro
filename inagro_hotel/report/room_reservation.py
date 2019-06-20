

from odoo import api, fields, models, tools

class Room_reservation_report(models.Model):
    _name = "reservation.report"
    _description = "Room Reservation Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    room_name = fields.Char('Room', readonly=True)
    room_type = fields.Char('Room Type', readonly=True)
    checkin = fields.Datetime('Checkin', readonly=True, oldname='date')
    checkout = fields.Datetime('Checkout', readonly=True, oldname='date')
    qty = fields.Float('Quantity', digits=(16, 0), readonly=True)
    unit_price = fields.Float('Unit Price', readonly=True)
    discounts_percent = fields.Float('Discount (%)', readonly=True)
    tax = fields.Float('Taxes', readonly=True)
    total = fields.Float('Total', readonly=True)
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True)


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
                min(sl.id) as id,
                sl.name as room_name,
                hrt.name as room_type,
                fl.checkin_date as checkin,
                fl.checkout_date as checkout,
                sl.product_uom_qty as qty,
                sl.price_unit as unit_price,
                sl.discount as discounts_percent,
                sl.price_tax as tax,
                sl.price_subtotal as total,
                sl.state as state
        """
        return select_str

    def _from(self):
        from_str = """
            hotel_folio_line fl
            LEFT JOIN sale_order_line sl on fl.order_line_id = sl.id
            LEFT JOIN hotel_room hr on sl.product_id = hr.product_id
            LEFT JOIN hotel_room_type hrt on hr.categ_id = hrt.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                sl.name,
                hrt.name,
                fl.checkin_date,
                fl.checkout_date,
                sl.product_uom_qty,
                sl.price_unit,
                sl.discount,
                sl.price_tax,
                sl.price_subtotal,
                sl.state
        """
        return group_by_str
