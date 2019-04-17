from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class inherit_budget(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'crossovered.budget'

    department_id = fields.Many2one('hr.department', string='Department',required=True, store=True)

    # @api.model
    # def create(self,values):
    # 	for line in values.get('crossovered_budget_line'):
    # 		# print('tt')
    # 		print(line,' fff')
    # 		print(line.planned_amount,' planned')
    # 		print(line.general_budget_id,' b name')

    # 		if line.general_budget_id.account_id.user_type_id == 'Expenses' and line.planned_amount > 0:
    # 			line.planned_amount = 0-line.planned_amount
    # 		return super(inherit_budget, self).create(values)


    

class inherit_CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    capex = fields.Boolean(string='Capex', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account 2',domain="[('is_budget','=',True)]")

    @api.model
    def create(self,values):

    	general_budget_id = self.env['account.budget.post'].search([('id', '=', int(values.get('general_budget_id')))])
    	
    	planned_amount = values.get('planned_amount')

    	print(general_budget_id.account_id.user_type_id,' ccccc')

    	if general_budget_id.account_id.user_type_id.name == 'Expenses' and planned_amount > 0:
    		values['planned_amount'] = 0 - planned_amount

    	# if general_budget_id.account_id.user_type_id

    	return super(inherit_CrossoveredBudgetLines, self).create(values)


    @api.multi
    def write(self, values):
    	super(inherit_CrossoveredBudgetLines, self).write(values)
    	
    	general_budget_id = self.env['account.budget.post'].search([('id', '=', int(self.general_budget_id))])
    	
    	planned_amount = self.planned_amount
    	if general_budget_id.account_id.user_type_id.name == 'Expenses' and planned_amount > 0:
    		values['planned_amount'] = 0 - planned_amount

    	return super(inherit_CrossoveredBudgetLines, self).write(values)

    



    
