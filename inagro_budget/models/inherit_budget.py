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
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account',domain="[('is_budget','=',True)]",required=True)


    _sql_constraints = [('analytic_account_id_uniq', 'unique (analytic_account_id)', 'Analytic account cannot used twice!')]
    _sql_constraints = [('analytic_account_id_uniq', 'check(1=1)', 'No error'),]

    # perbaiki function ini !!!!
    # arahkan account dari general account_ids ke account_id.id
    @api.multi
    def _compute_practical_amount(self):
        print('practical amount')
        for line in self:
            acc_ids = line.general_budget_id.account_id.id
            date_to = line.date_to
            date_from = line.date_from
            if line.analytic_account_id.id:
                analytic_line_obj = self.env['account.analytic.line']
                domain = [('account_id', '=', line.analytic_account_id.id),
                          ('date', '>=', date_from),
                          ('date', '<=', date_to),
                          ]
                if acc_ids:
                    domain += [('general_account_id', 'in', [acc_ids])]

                where_query = analytic_line_obj._where_calc(domain)
                analytic_line_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(amount) from " + from_clause + " where " + where_clause

            else:
                aml_obj = self.env['account.move.line']
                domain = [('account_id', 'in',
                           [line.general_budget_id.account_id.id]),
                          ('date', '>=', date_from),
                          ('date', '<=', date_to)
                          ]
                where_query = aml_obj._where_calc(domain)
                aml_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.practical_amount = self.env.cr.fetchone()[0] or 0.0
    
    @api.model
    def create(self,values):

    	general_budget_id = self.env['account.budget.post'].search([('id', '=', int(values.get('general_budget_id')))])
    	
    	planned_amount = values.get('planned_amount')

    	print(general_budget_id.account_id.user_type_id,' ccccc')

    	if general_budget_id.account_id.user_type_id.name != 'Income' and planned_amount > 0:
    		values['planned_amount'] = 0 - planned_amount

    	# if general_budget_id.account_id.user_type_id

    	return super(inherit_CrossoveredBudgetLines, self).create(values)


    @api.multi
    def write(self, values):
    	super(inherit_CrossoveredBudgetLines, self).write(values)
    	
    	general_budget_id = self.env['account.budget.post'].search([('id', '=', int(self.general_budget_id))])
    	
    	planned_amount = self.planned_amount
    	if general_budget_id.account_id.user_type_id.name != 'Income' and planned_amount > 0:
    		values['planned_amount'] = 0 - planned_amount

    	return super(inherit_CrossoveredBudgetLines, self).write(values)

    



    
