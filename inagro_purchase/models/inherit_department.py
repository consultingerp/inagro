from odoo import api, fields, models, _ 
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError

# _business_type = [
#     ('operasional', 'Operasional'),
#     ('agribisnis', 'Agribisnis')
# ]

class inherit_department_inagro(models.Model):

    # _name = 'sprogroup.purchase.request'
    _inherit = 'hr.department'

    bis_type = fields.Many2one('bis.type', 'Business Type', required=True,
        default=lambda self: self.env['bis.type'].search([('id','=',1)]))
    
    # bis_type = fields.Selection(selection=_business_type,
    #                          string='Business Type',
    #                          index=True,
    #                          required=True,
    #                          default='operasional')