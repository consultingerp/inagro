# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import namedtuple
import json
import time
from datetime import date

from itertools import groupby
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter


class inagro_agriculture_PickingType(models.Model):
    _inherit = "stock.picking.type"

    is_cultivation = fields.Boolean(
        string='Is Cultivation?',
        copy=True
    )

    is_harvest = fields.Boolean(
        string='Is Harvest?',
        copy=True
    )