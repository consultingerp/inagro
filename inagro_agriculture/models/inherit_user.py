from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError



class inagro_agriculture_inherit_user(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'res.users'
    commodity_type_ids = fields.Many2many('commodity.type',relation="user_commodity_type", column1="user_id", culomn2="commodity_type_id", string='Commodity_type')



    
