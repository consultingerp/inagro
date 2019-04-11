from odoo import api, fields, models, _ 
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError

_business_type = [
    ('operasional', 'Operasional'),
    ('agribisnis', 'Agribisnis')
]

class inherit_employee_inagro(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'hr.employee'
    
    bis_type = fields.Selection(selection=_business_type,
                             string='Business Type',
                             index=True,
                             required=True,
                             default='operasional')


  



    
