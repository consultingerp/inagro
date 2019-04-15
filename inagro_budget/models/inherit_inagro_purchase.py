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
    ('rejected', 'Cancel'),
    ('done', 'Done'),
    ('to_po', 'To Order')
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


class inherit_PR_line(models.Model):
    _inherit = 'sprogroup.purchase.request.line'

    budget_line_id = fields.Many2one('crossovered.budget.lines', string='Budget', store=True)


    



    
