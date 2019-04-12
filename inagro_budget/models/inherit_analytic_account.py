from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class inherit_analytic_account(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'account.analytic.account'

    department_id = fields.Many2one('hr.department', string='Department',required=False, store=True)

    



    
