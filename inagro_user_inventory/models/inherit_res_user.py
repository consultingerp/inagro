from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError



class inherit_user(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'res.users'

    warehouse_ids = fields.Many2many('stock.picking.type', string='Default Warehouse Operations')



    
