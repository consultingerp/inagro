# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class inherit_ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    corporate_approve = fields.Float('Corporate Approve', readonly=False)
    
