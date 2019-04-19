from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp


class inherit_AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    
    def _prepare_invoice_line_from_po_line(self, line):
        if line.product_id.purchase_method == 'purchase':
            qty = line.product_qty - line.qty_invoiced
        else:
            qty = line.qty_received - line.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
            qty = 0.0
        taxes = line.taxes_id
        invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes, line.product_id, line.order_id.partner_id)
        invoice_line = self.env['account.invoice.line']
        date = self.date or self.date_invoice
        data = {
            'purchase_line_id': line.id,
            'name': line.order_id.name + ': ' + line.name,
            'origin': line.order_id.origin,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id,
            'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
            'price_unit': line.order_id.currency_id._convert(
                line.price_unit, self.currency_id, line.company_id, date or fields.Date.today(), round=False),
            'quantity': qty,
            'discount': 0.0,
            'account_analytic_id': line.account_analytic_id.id,
            'analytic_tag_ids': line.analytic_tag_ids.ids,
            'invoice_line_tax_ids': invoice_line_tax_ids.ids
        }
        account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
        if account:
            data['account_id'] = line.budget_line_id.general_budget_id.account_id.id
            data['budget_line_id'] = line.budget_line_id.id
        return data

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open

        # kondisi pada saat validate vendor bill
        if self.type == 'in_invoice':
            print('type in_invoice')
            for line_invoice in self.invoice_line_ids:
                print(line_invoice.product_id.is_asset,' asset product')
                print(line_invoice.product_id.product_tmpl_id.is_asset,' asset template product')
                print(len(line_invoice.asset_category_id),' id asset')

                # product yg merupakan asset harus memiliki kategory asset pada saat validate vendor bill
                if (line_invoice.product_id.is_asset==True or line_invoice.product_id.product_tmpl_id.is_asset==True) and len(line_invoice.asset_category_id) <= 0:
                    raise UserError(_('Item '+line_invoice.product_id.name+' must have asset category !'))

            # exit()


            # cek apakah budget masih ada
            self.env.cr.execute("""
                SELECT DISTINCT budget_line_id,sum(price_subtotal) as sum_subtotal
                FROM
                    account_invoice_line
                WHERE
                    invoice_id = %s
                GROUP BY budget_line_id"""%(int(self.id)))
            line_distinct = self.env.cr.dictfetchall()

            for line in line_distinct:
                print(line,' line')
                print(line['budget_line_id'],' line2')
                budget = self.env['crossovered.budget.lines'].search([('id', '=', int(line['budget_line_id']))])
                print(budget,' budget')
                planned_budget = budget.planned_amount
                sum_subtotal_pr = line['sum_subtotal']
                new_practical_amount = budget.practical_amount-sum_subtotal_pr

                print(planned_budget,' plan')
                print(sum_subtotal_pr,' sum_subtotal_pr')
                print(new_practical_amount,' new_practical_amount') 

                # exit()

                if new_practical_amount < planned_budget:
                    raise UserError(_('Value from '+str(budget.name)+' is not enough, plese use another budget !'))


        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: not inv.partner_id):
            raise UserError(_("The field Vendor is required, please complete it to validate the Vendor Bill."))
        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        if to_open_invoices.filtered(lambda inv: not inv.account_id):
            raise UserError(_('No account was found to create the invoice, be sure you have installed a chart of account.'))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()


class inherit_AccountInvoiceLine(models.Model):
    """ Override AccountInvoice_line to add the link to the purchase order line it is related to"""
    _inherit = 'account.invoice.line'

    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget', store=True,domain="[('crossovered_budget_id.state','=','validate')]")
    account_asset_id = fields.Many2one('account.account', string='Account Asset',related='asset_category_id.account_asset_id', domain=[('deprecated', '=', False)],
        help="The income or expense account related to the selected product.")
    capex = fields.Boolean(string='Capex', store=True,related='budget_line_id.capex')

    @api.onchange('asset_category_id')
    def onchange_asset_category_id(self):
        if self.invoice_id.type == 'out_invoice' and self.asset_category_id:
            self.account_asset_id = self.asset_category_id.account_asset_id.id
        elif self.invoice_id.type == 'in_invoice' and self.asset_category_id:
            self.account_asset_id = self.asset_category_id.account_asset_id.id


    @api.one
    def asset_create(self):
        if self.asset_category_id:
            vals = {
                'name': self.name,
                'code': self.invoice_id.number or False,
                'category_id': self.asset_category_id.id,
                'value': self.price_subtotal_signed,
                'partner_id': self.invoice_id.partner_id.id,
                'company_id': self.invoice_id.company_id.id,
                'currency_id': self.invoice_id.company_currency_id.id,
                'date': self.invoice_id.date_invoice,
                'invoice_id': self.invoice_id.id,
            }
            print(vals,'vals')


            changed_vals = self.env['account.asset.asset'].onchange_category_id_values(vals['category_id'])
            print(changed_vals,' changed_vals')
            
            vals.update(changed_vals['value'])
            asset = self.env['account.asset.asset'].create(vals)
            if self.asset_category_id.open_asset:
                asset.validate()
        return True