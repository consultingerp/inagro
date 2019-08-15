# See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
from odoo.exceptions import ValidationError, UserError
import pytz


class inherit_HotelReservation(models.Model):

    _inherit = "hotel.reservation"

    # is_company = fields.Boolean(string='Is a Company',related="partner_id.is_company",store=True)
    partner_company_type = fields.Selection(string='Company Type',related="partner_id.company_type",
        selection=[('person', 'Individual'), ('company', 'Company')],store=True)


