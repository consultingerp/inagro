import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError

class inagro_crm_Lead(models.Model):
    _inherit = "crm.lead"

    tuition_fee = fields.Monetary('Tuition fee',currency_field='company_currency')
    number_student = fields.Float(string='Number of students', store=True,digits=(16,0))