from odoo import api, fields, models, _ 
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class bis_type(models.Model):

    # _name = 'sprogroup.purchase.request'
    _name = 'bis.type'
    
    name = fields.Char(String='Business Type')
    direktur = fields.Many2one('hr.employee', 'Direktur')