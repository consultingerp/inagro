

from odoo import api, fields, models, tools

class inagro_agri_cultivation_plan_organic_report(models.Model):
    _name = "cultivation.plan_organic_report"
    _description = "Cultivation Plan Organic Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    year = fields.Char('Year', readonly=True)
    name_varieties = fields.Char('Varieties', readonly=True)
    name_category = fields.Char('Description', readonly=True)
    date_plan_organic = fields.Date('Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True)


    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            )""" 
            % (self._table, self._select(), self._from(), self._group_by()))

    def _select(self):
        select_str = """
            SELECT
                min(cl.id) as id,
                cl. YEAR,
                cv. NAME as name_varieties,
                cc. NAME AS name_category,
                cl. STATE,
                cpd. NAME AS date_plan_organic
        """
        return select_str

    def _from(self):
        from_str = """
            cultivation_plan_line cl
            LEFT JOIN cultivation_plan cp ON cl.line_id = cp. ID
            LEFT JOIN crop_varieties cv ON cl. NAME = cv. ID
            LEFT JOIN crop_category cc ON cl.category = cc. ID
            LEFT JOIN cultivation_plan_line_organik_date_rel cdo ON cl. ID = cdo.organic_date
            LEFT JOIN cultivation_plan_line_date cpd ON cdo.cultivation_plan_line_date_id = cpd. ID
            WHERE cpd. NAME is NOT NULL
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                cl. YEAR,
                cv. NAME,
                cc. NAME,
                cl. STATE,
                cpd. NAME
        """
        return group_by_str




