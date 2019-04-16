from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError


class inherit_product(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'product.product'

    is_asset = fields.Boolean('Is Asset?', store=True)



class inherit_template(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'product.template'

    is_asset = fields.Boolean('Is Asset?', store=True)

    

    



    
