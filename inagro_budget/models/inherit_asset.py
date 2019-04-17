# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class inherit_AccountAssetCategory_budget(models.Model):
    _inherit = 'account.asset.category'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',domain="['&',('is_asset','=',True),('company_id', '=', company_id)]")
