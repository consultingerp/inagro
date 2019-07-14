

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
    duration_day = fields.Float('Number of days', digits=(16, 0), readonly=True)
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
                CASE
                  WHEN hrt. NAME  = 'Function Rooms' THEN
                     (to_date(to_char(fl.checkout_date,'yyyy-mm-dd'),'yyyy-mm-dd')-to_date(to_char(fl.checkin_date,'yyyy-mm-dd'),'yyyy-mm-dd'))+1
                  ELSE
                     (to_date(to_char(fl.checkout_date,'yyyy-mm-dd'),'yyyy-mm-dd')-to_date(to_char(fl.checkin_date,'yyyy-mm-dd'),'yyyy-mm-dd'))
                  END
                as duration_day,
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



class info_booking_marketing(models.Model):
    _name = "info.booking"
    _description = "Info booking"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    reservation_no = fields.Char('Reservation No', readonly=True)
    nama_partner = fields.Char('Customer', readonly=True)
    checkin = fields.Datetime('Checkin', readonly=True, oldname='date')
    checkout = fields.Datetime('Checkout', readonly=True, oldname='date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel'),
        ('done', 'Done'),
        ], string='Status', readonly=True)
    nama_user = fields.Char('User', readonly=True)
    nama_ruangan = fields.Char('Room', readonly=True)
    room_type = fields.Char('Room Category', readonly=True)

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
                min(hr.id) as id,
                hr.reservation_no,
                rp. NAME AS nama_partner,
                hr.checkin,
                hr.checkout,
                hr. STATE,
                rpu. NAME AS nama_user,
                pt. NAME AS nama_ruangan,
                rm_tp.name as room_type
        """
        return select_str

    def _from(self):
        from_str = """
            hotel_reservation hr
            LEFT JOIN res_partner rp ON hr.partner_id = rp. ID
            LEFT JOIN res_users ru ON hr.create_uid = ru. ID
            LEFT JOIN res_partner rpu ON ru.partner_id = rpu. ID
            LEFT JOIN hotel_reservation_line hrl ON hr. ID = hrl.line_id
            LEFT JOIN hotel_reservation_line_room_rel hrl_r ON hrl. ID = hrl_r.hotel_reservation_line_id
            LEFT JOIN hotel_room room ON hrl_r.room_id = room. ID
            LEFT JOIN hotel_room_type rm_tp on room.categ_id = rm_tp.id
            LEFT JOIN product_product pp ON room.product_id = pp. ID
            LEFT JOIN product_template pt ON pp.product_tmpl_id = pt. ID
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                hr.reservation_no,
                rp. NAME,
                hr.checkin,
                hr.checkout,
                hr. STATE,
                rpu. NAME,
                pt. NAME,
                rm_tp.name
        """
        return group_by_str
