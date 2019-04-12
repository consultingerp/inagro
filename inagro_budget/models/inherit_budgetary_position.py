from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class inherit_budgetary_position(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'account.budget.post'

    department_id = fields.Many2one('hr.department', string='Department',required=True, store=True)
    account_id = fields.Many2one('account.account', string='Account',required=True, store=True, domain=[('deprecated', '=', False)])

    def _check_account_ids(self, vals):
        print('tes')
        # Raise an error to prevent the account.budget.post to have not specified account_ids.
        # This check is done on create because require=True doesn't work on Many2many fields.
        # if 'account_ids' in vals:
        #     account_ids = self.resolve_2many_commands('account_ids', vals['account_ids'])
        # else:
        #     account_ids = self.account_ids
        # if not account_ids:
        #     raise ValidationError(_('The budget must have at least one account.'))

    



    
