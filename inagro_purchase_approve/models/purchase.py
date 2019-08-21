# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp


class PurchaseOrder_inherit_approve(models.Model):
    _inherit = "purchase.order"

    
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('spv_confirm', 'SPV Confirm'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')


    @api.multi
    def btn_spv_confirm(self, force=False):
        # print (len(self.partner_id),'nnn')
        if len(self.partner_id) == 0:
            raise UserError(_('Vendor has not been selected.'))
        else:
            self.write({'state': 'spv_confirm', 'date_approve': fields.Date.context_today(self)})
        return {}

    @api.multi
    def print_quotation(self):
        # self.write({'state': "sent"})
        return self.env.ref('purchase.report_purchase_quotation').report_action(self)

    # @api.multi
    # def button_approve(self, force=False):
    #     self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
    #     self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
    #     return {}

    @api.multi
    def button_confirm(self):
        # print('tes confirm')
        for order in self:
            order.confirm_id = self.env['res.users'].browse(self.env.uid)
            print(order.confirm_id,'dddddddddd')
            if order.state not in ['spv_confirm', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('inagro_budget.purchase_corporate'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True