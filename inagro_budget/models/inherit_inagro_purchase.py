from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError

_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be approved'),
    # ('leader_approved', 'Leader Approved'),
    ('manager_approved', 'Manager Approved'),
    # ('dir_approved', 'Direktur Approved'),
    ('done', 'Done'),
    ('to_po', 'To Order'),
    ('rejected', 'Cancel')
]

class inherit_inagro_PurchaseRequest(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'sprogroup.purchase.request'

    # @api.model
    # def _get_default_requested_by(self):
    #     print('tes')
    #     return self.env['res.users'].browse(self.env.uid)

    code = fields.Char('Code', size=32, required=False)
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')

    @api.one
    @api.depends('requested_by')
    def _compute_bis_type(self):
        if (self.requested_by.id == False):
            self.department_id = None
            return

        print(self.env.uid,'uid login')
        # print(self.env.uid.employee_id,' bis_type')

        employee = self.env['hr.employee'].search([('work_email', '=', self.requested_by.email)])
        if (len(employee) > 0):
            self.bis_type = employee[0].department_id.bis_type
        else:
            self.bis_type = None

    bis_type = fields.Many2one('bis.type', 'Business Type', compute='_compute_bis_type', store=True, required=False)

    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        current_user = self.env['res.users'].browse(self.env.uid)
        for rec in self:
            if rec.state == 'draft' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_user'):
                rec.is_editable = True
            elif rec.state == 'to_approve' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_manager'):
                rec.is_editable = True
            # elif rec.state == 'manager_approved' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_direktur'):
            #     rec.is_editable = True
            else:
                rec.is_editable = False

    @api.multi
    def button_to_approve(self):

        self.env.cr.execute("""
            SELECT DISTINCT budget_line_id,sum(price_subtotal) as sum_subtotal
            FROM
                sprogroup_purchase_request_line
            WHERE
                request_id = %s
            GROUP BY budget_line_id"""%(int(self.id)))
        line_distinct = self.env.cr.dictfetchall()

        for line in line_distinct:
            print(line,' line')
            print(line['budget_line_id'],' line2')
            budget = self.env['crossovered.budget.lines'].search([('id', '=', int(line['budget_line_id']))])
            planned_budget = budget.planned_amount
            sum_subtotal_pr = line['sum_subtotal']
            new_practical_amount = budget.practical_amount-sum_subtotal_pr

            print(planned_budget,' plan')
            print(sum_subtotal_pr,' sum_subtotal_pr')
            print(new_practical_amount,' new_practical_amount') 

            if new_practical_amount < planned_budget:
                raise UserError(_('Value from '+budget.name+' is not enough, plese use another budget !'))

        return self.write({'state': 'to_approve'})

    # @api.multi
    # def button_manager_approved(self):
    #     print('mgr app')
    #     exit()
    #     return self.write({'state': 'manager_approved'})

    @api.multi
    def make_purchase_quotation(self):
        view_id = self.env.ref('purchase.purchase_order_form')

        # vals = {
        #     'partner_id': partner.id,
        #     'picking_type_id': self.rule_id.picking_type_id.id,
        #     'company_id': self.company_id.id,
        #     'currency_id': partner.property_purchase_currency_id.id or self.env.user.company_id.currency_id.id,
        #     'dest_address_id': self.partner_dest_id.id,
        #     'origin': self.origin,
        #     'payment_term_id': partner.property_supplier_payment_term_id.id,
        #     'date_order': purchase_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
        #     'fiscal_position_id': fpos,
        #     'group_id': group
        # }

        order_line = []
        for line in self.line_ids:
            product = line.product_id
            fpos = self.env['account.fiscal.position']
            if self.env.uid == SUPERUSER_ID:
                company_id = self.env.user.company_id.id
                taxes_id = fpos.map_tax(line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
            else:
                taxes_id = fpos.map_tax(line.product_id.supplier_taxes_id)

            product_line = (0, 0, {'product_id' : line.product_id.id,
                                    'budget_line_id' : line.budget_line_id.id,
                                    'account_analytic_id' : line.analytic_account_id.id,
                                   'state' : 'draft',
                                   'product_uom' : line.product_id.uom_po_id.id,
                                    'price_unit' : line.price_unit,
                                   'date_planned' :  datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                   # 'taxes_id' : ((6,0,[taxes_id.id])),
                                   'product_qty' : line.product_qty,
                                   'name' : line.product_id.name
                                   })
            order_line.append(product_line)

        rfq_sequence = self.env['ir.sequence'].next_by_code('purchase.order')

        print(rfq_sequence,' sequence rfq')

        print('tes sequence')

        vals = {
            'order_line' : order_line,
            'state': 'draft',
            'pr_id': self.id,
            # 'name': self.name,
            # 'name': _('New Quotation'),
            'name': rfq_sequence,
            'bis_type': self.bis_type.id,
            'picking_type_id' : 1,
            'requested_by': int(self.requested_by),
            'department_id': int(self.department_id)
        }
        
        po = self.env['purchase.order'].create(vals)

        self.write({'state': 'done'})



class inherit_PR_line(models.Model):
    _inherit = 'sprogroup.purchase.request.line'

    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget', store=True,domain="[('crossovered_budget_id.state','=','validate')]")
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic',related='budget_line_id.analytic_account_id', store=True)

    


    



    
