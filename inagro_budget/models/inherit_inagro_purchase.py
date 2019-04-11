from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class inherit_inagro_PurchaseRequest(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'sprogroup.purchase.request'

    code = fields.Char('Code', size=32, required=False)

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



    



    
