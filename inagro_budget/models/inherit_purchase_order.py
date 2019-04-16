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


class inherit_PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
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


class inherit_PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget', store=True,domain="[('crossovered_budget_id.state','=','validate')]")
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',related='budget_line_id.analytic_account_id', store=True)