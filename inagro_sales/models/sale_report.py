# -*- coding: utf-8 -*-

from odoo import models, fields, api


class inagro_sale_report(models.Model):
    _inherit = 'sale.report'

    validity_date = fields.Datetime('Validity Date', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['validity_date'] = ",(s.validity_date + 1) as validity_date"
        groupby += ', s.validity_date'
        return super(inagro_sale_report, self)._query(with_clause, fields, groupby, from_clause)
    
    