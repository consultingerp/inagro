# -*- coding: utf-8 -*-

from odoo import models, fields, api


class inherit_purchase_report(models.Model):
    _inherit = 'purchase.report'

    department_id = fields.Many2one('hr.department', 'Departement', readonly=True)
    po_number = fields.Char('PO Number', readonly=True)

    def _select(self):
        return super(inherit_purchase_report, self)._select() + ", s.department_id,s.name as po_number"

    def _from(self):
        return super(inherit_purchase_report, self)._from() + "left join hr_department hr_d on (s.department_id=hr_d.id)"

    def _group_by(self):
        return super(inherit_purchase_report, self)._group_by() + ", s.department_id,s.name"
    
    