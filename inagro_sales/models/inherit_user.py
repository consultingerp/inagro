from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError



class inagro_sales_inherit_user(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'res.users'

    sales_warehouse_ids = fields.Many2many('stock.warehouse', string='Default Warehouse')
    sales_child_ids = fields.Many2many('res.users',relation="sale_child_parent", column1="sales_parent", culomn2="sales_child", string='Subordinate Marketing')



    
