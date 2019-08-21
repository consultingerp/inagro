# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class signature_PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    confirm_id = fields.Many2one('res.users','Confirm By',required=False)

    @api.multi
    def button_confirm(self):
        print(self.partner_id,'dddddddddd nnn')


        for order in self:
            order.confirm_id = self.env['res.users'].browse(self.env.uid)
            print(order.confirm_id,'dddddddddd')

            if len(order.partner_id) <= 0:
                raise UserError(_('Vendor has not been selected.'))
            else:
                # print('ada')
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step'\
                        or (order.company_id.po_double_validation == 'two_step'\
                            and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
        return True
