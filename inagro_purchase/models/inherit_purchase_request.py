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
    ('manager_approved', 'Purchase Approved'),
    ('dir_approved', 'Direktur Approved'),
    ('rejected', 'Cancel'),
    ('done', 'Done'),
    ('to_po', 'To Order')
]

_business_type = [
    ('operasional', 'Operasional'),
    ('agribisnis', 'Agribisnis')
]

class inherit_PurchaseRequest(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'sprogroup.purchase.request'


    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code('sprogroup.purchase.request')

    name = fields.Char('PR Number', required=True, index=True, copy=False, default='New')
    code = fields.Char('Code', size=32, required=False)
    assigned_to = fields.Many2one('res.users', 'Approver', required=False,
                                  track_visibility='onchange')


    date_start = fields.Date('Request date',
                             help="Date when the user initiated the request.",
                             default=fields.Date.context_today,
                             track_visibility='onchange')

    
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')

    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)

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

    # bis_type = fields.Many2one('hr.department', string='Department', compute='_compute_department', store=True,)
    # bis_type = fields.Selection(selection=_business_type,
    #                          string='Business Type',
    #                          index=True,
    #                          required=True,
    #                          compute='_compute_bis_type',
    #                          default='operasional')

    bis_type = fields.Many2one('bis.type', 'Business Type', compute='_compute_bis_type', store=True, required=True)

    @api.depends('line_ids.price_unit')
    def _amount_all(self):
        for order in self:
            amount_total = 0.0
            for line in order.line_ids:
                amount_total += line.price_subtotal
            order.amount_total = amount_total
            order.update({
                'amount_total': order.currency_id.round(int(amount_total))
            })

    
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')


    @api.multi
    def button_dir_approved(self):
        return self.write({'state': 'dir_approved'})

    @api.multi
    @api.depends('state')
    def _compute_is_editable(self):
        current_user = self.env['res.users'].browse(self.env.uid)
        for rec in self:
            if rec.state == 'draft' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_user'):
                rec.is_editable = True
            elif rec.state == 'to_approve' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_manager'):
                rec.is_editable = True
            elif rec.state == 'manager_approved' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_direktur'):
                rec.is_editable = True
            else:
                rec.is_editable = False

    @api.one
    @api.depends('state')
    def _compute_can_reject(self):
        # self.can_reject = (self.can_leader_approved or self.can_manager_approved)
        current_user = self.env['res.users'].browse(self.env.uid)
        if self.state == 'to_approve' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_manager'):
            self.can_reject = True
        elif self.state == 'manager_approved' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_direktur'):
            self.can_reject =True
        else:
            self.can_reject = False

    @api.multi
    def unlink(self):
        for order in self:
            if order.state != 'draft':
                raise UserError(_('To delete, state must be Draft'))
        return super(inherit_PurchaseRequest, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # print(self.name,' name')
            # new = self.env['ir.sequence'].next_by_code('sprogroup.purchase.request')
            # print(new,' new')
            vals['name'] = self.env['ir.sequence'].next_by_code('sprogroup.purchase.request')
        return super(inherit_PurchaseRequest, self).create(vals)

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

        # return {
        #     'name': _('New Quotation'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'purchase.order',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'target': 'new',
        #     'view_id': view_id.id,
        #     'views': [(view_id.id, 'form')],
        #     'context': {
        #         'default_order_line': order_line,
        #         'default_state': 'draft',
        #         'default_pr_id': self.id,
        #         'default_requested_by': int(self.requested_by),
        #         'default_department_id': int(self.department_id),

        #     }
        # }





class inherit_PurchaseRequest_line(models.Model):
    _inherit = 'sprogroup.purchase.request.line'

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('purchase_ok', '=', True)], required=True)

    currency_id = fields.Many2one(related='request_id.currency_id', store=True, string='Currency', readonly=True)
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure', required=True, related='product_id.uom_po_id', store=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for rec in self:
            rec.price_subtotal = (int(rec.product_qty) or 0) * (int(rec.price_unit) or 0)
            # print(rec.price_subtotal,' xx')

    def _compute_is_editable(self):
        current_user = self.env['res.users'].browse(self.env.uid)
        for rec in self:
            if rec.request_id.state == 'draft' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_user'):
                rec.is_editable = True
            elif rec.request_id.state == 'to_approve' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_manager'):
                rec.is_editable = True
            elif rec.request_id.state == 'manager_approved' and current_user.has_group('sprogroup_purchase_request.group_sprogroup_purchase_request_direktur'):
                rec.is_editable = True
            else:
                rec.is_editable = False


class inherit_PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    partner_id = fields.Many2one('res.partner', string='Vendor', required=False, states=READONLY_STATES, change_default=True, track_visibility='always')
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, states=READONLY_STATES,\
        default=lambda self: self.env.user.company_id.currency_id.id)
    pr_id = fields.Many2one('sprogroup.purchase.request', string='PR Number', required=True, change_default=True, track_visibility='always')

    requested_by = fields.Many2one('res.users','Requested by',required=False)
    department_id = fields.Many2one('hr.department', string='Department',required=False, store=True)

    bis_type = fields.Many2one('bis.type', 'Business Type', store=True)

    # pay_term = fields.Char('Payment Term')

    @api.onchange('pr_id')
    def onchange_pr_id(self):
        self.requested_by = self.pr_id.requested_by
        self.department_id = self.pr_id.department_id

        order_line = []
        for line in self.pr_id.line_ids:
            product_line = (0, 0, {'product_id' : line.product_id.id,
                                       'state' : 'draft',
                                       'product_uom' : line.product_id.uom_po_id.id,
                                        'price_unit' : line.price_unit,
                                       'date_planned' :  datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                       # 'taxes_id' : ((6,0,[taxes_id.id])),
                                       'product_qty' : line.product_qty,
                                       'name' : line.product_id.name
                                       })
            order_line.append(product_line)

        self.order_line = order_line
        self.bis_type = self.pr_id.bis_type

    @api.multi
    def button_confirm(self):
        # print(self.partner_id,'dddddddddd')

        for order in self:

            print(order.partner_id,'dddddddddd')

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


# class inherit_PurchaseOrder_line(models.Model):
#     _inherit = "purchase.order.line"

#     product_qty = fields.Float(string='Quantity',digits=(16,2), required=True)



    
