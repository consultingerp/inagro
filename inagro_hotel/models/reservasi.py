# See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
from odoo.exceptions import ValidationError, UserError
import pytz


class inherit_HotelReservation(models.Model):

#     _inherit = "hotel.reservation"
    _name = "hotel.reservation"
    _inherit = ['hotel.reservation','mail.thread']

    # is_company = fields.Boolean(string='Is a Company',related="partner_id.is_company",store=True)
    partner_company_type = fields.Selection(string='Company Type',related="partner_id.company_type",
        selection=[('person', 'Individual'), ('company', 'Company')],store=True)

    # warehouse_id = fields.Many2one('stock.warehouse', 'Hotel', readonly=True,
    #                                index=True,
    #                                required=True,
    #                                states={'draft': [('readonly', False)]})




# class inherit_Hotel_Folio(models.Model):

#     # _inherit = "hotel.folio"
#     # _inherit = ['mail.thread']
#     _name = "hotel.folio"
#     _inherit = ['hotel.folio','mail.thread']


class inagro_hotel_inherit_SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('name','order_line','order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        # print('amount all hotel folio')
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax

            # print(amount_untaxed,' mmmm')
            if amount_untaxed > 0:
                # print(amount_untaxed,' mmmmtee')
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_untaxed + amount_tax,
                })

                # order.write({'amount_untaxed': amount_untaxed})

            # order.amount_untaxed = amount_untaxed
            # order.amount_tax = amount_tax
            # order.amount_total = amount_untaxed + amount_tax

            # print(order.amount_untaxed,' order ttttttttttttttttttttttttttttttttttttttttttttt ttttttttttttttttttttttttttttttt yyyyyyyy')

    @api.model
    def create(self, vals):

        new_id = super(inagro_hotel_inherit_SaleOrder, self).create(vals)
        self._amount_all()

        return new_id

    # @api.model
    # def write(self, vals):

    #     new_id = super(inagro_hotel_inherit_SaleOrder, self).write(vals)
    #     self._amount_all()

    #     return new_id

