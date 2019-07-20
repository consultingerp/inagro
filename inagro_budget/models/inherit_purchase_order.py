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

        # dn cut cek to budget
        # self.env.cr.execute("""
        #     SELECT DISTINCT budget_line_id,sum(price_subtotal) as sum_subtotal
        #     FROM
        #         purchase_order_line
        #     WHERE
        #         order_id = %s
        #     GROUP BY budget_line_id"""%(int(self.id)))
        # line_distinct = self.env.cr.dictfetchall()

        # for line in line_distinct:
        #     print(line,' line')
        #     print(line['budget_line_id'],' line2')
        #     budget = self.env['crossovered.budget.lines'].search([('id', '=', int(line['budget_line_id']))])
        #     print(budget,' budget')
        #     planned_budget = budget.planned_amount
        #     sum_subtotal_pr = line['sum_subtotal']
        #     new_practical_amount = budget.practical_amount-sum_subtotal_pr

        #     print(planned_budget,' plan')
        #     print(sum_subtotal_pr,' sum_subtotal_pr')
        #     print(new_practical_amount,' new_practical_amount') 

        #     if new_practical_amount < planned_budget:
        #         raise UserError(_('Value from '+budget.name+' is not enough, plese use another budget !'))
        # dn cut cek to budget
        # exit()

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

    @api.multi
    def _add_supplier_to_product(self):
        # print('tessss')
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        for line in self.order_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if partner not in line.product_id.seller_ids.mapped('name') and len(line.product_id.seller_ids) <= 10:
                currency = partner.property_purchase_currency_id or self.env.user.company_id.currency_id
                company = line.company_id or self.env.user.company_id
                # print(company,'cc')
                line.write({'company_id': int(company)})
                # line.company_id = company
                # print(line.price_unit,'line.price_unit')
                # print(currency,'currency')
                # print(line.company_id,'line.company_id')

                supplierinfo = {
                    'name': partner.id,
                    'sequence': max(line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                    'product_uom': line.product_uom.id,
                    'min_qty': 0.0,
                    'price': self.currency_id._convert(line.price_unit, currency, company, line.date_order or fields.Date.today(), round=False),
                    'currency_id': currency.id,
                    'delay': 0,
                }

                # print(supplierinfo)
                # exit()
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break

    pr_id = fields.Many2one('sprogroup.purchase.request', string='PR Number',domain="[('state','=','done')]", required=True, change_default=True, track_visibility='always')
    @api.onchange('pr_id')
    def onchange_pr_id(self):
        self.requested_by = self.pr_id.requested_by
        self.department_id = self.pr_id.department_id

        purchase_order = self.env['purchase.order'].search([('pr_id', '=', self.pr_id.id)])
        product_use = []
        for po in purchase_order:
            for pl in po.order_line:
                product_use.append(pl.product_id.id)
       
        # if self.pr_id.id
        if self.pr_id.id != False:
            order_line = []
            for line in self.pr_id.line_ids.search(['&',('request_id', '=', int(self.pr_id)),('product_id', 'not in', product_use)]):
                product_line = (0, 0, {'product_id' : line.product_id.id,
                                           'state' : 'draft',
                                           'product_uom' : line.product_id.uom_po_id.id,
                                            # 'price_unit' : line.price_unit,
                                           'date_planned' :  datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                           # 'taxes_id' : ((6,0,[taxes_id.id])),
                                           'currency_id' : line.currency_id,
                                           'company_id' : self.env.user.company_id,
                                           'product_qty' : line.product_qty,
                                           'name' : line.product_id.name
                                           })
                # print(product_line,'pl')
                order_line.append(product_line)

            self.order_line = order_line
            self.bis_type = self.pr_id.bis_type

class inherit_PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget', store=True,domain="[('crossovered_budget_id.state','=','validate')]")
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',related='budget_line_id.analytic_account_id', store=True)