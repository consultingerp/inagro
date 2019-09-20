

from odoo import api, fields, models, tools

class inagro_agri_activity_report(models.Model):
    _name = "crop.activity_report"
    _description = "Crop activity Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    name_act = fields.Char('activity', readonly=True)
    desc_act = fields.Char('Description', readonly=True)
    farmer = fields.Char('Farmer', readonly=True)
    crop_code = fields.Char('Crop Code', readonly=True)
    varietas = fields.Char('Varieties', readonly=True)
    category = fields.Char('Category', readonly=True)
    area = fields.Char('Area', readonly=True)
    date_acti = fields.Datetime('Date', readonly=True)
    state_act = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),('cancel', 'Cancel'), ('done', 'Done')],'State', readonly=True)


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
                min(cal.id) as id,
                cm.name as name_act,
                cal.description as desc_act,
                rp.display_name AS farmer,
                flc. NAME AS crop_code,
                cv. NAME AS varietas,
                cc. NAME AS category,
                area. NAME AS area,
                ca. date as date_acti,
                ca.state as state_act
        """
        return select_str

    def _from(self):
        from_str = """
            crop_activity_line cal
            LEFT JOIN crop_masteractivity cm ON cal."name" = cm. ID
            LEFT JOIN res_partner rp ON cal.farmer_id = rp."id"
            LEFT JOIN crop_activity ca ON cal.line_id = ca. ID
            LEFT JOIN farmer_location_crops flc ON ca. NAME = flc."id"
            LEFT JOIN crop_varieties cv ON ca.varieties_id = cv. ID
            LEFT JOIN crop_category cc ON ca.category_id = cc. ID
            LEFT JOIN res_partner area ON ca.area_location_id = area."id"
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                cm.NAME,
                cal.description,
                rp.display_name,
                flc. NAME,
                cv. NAME,
                cc. NAME,
                area. NAME,
                ca. DATE,
                ca."state"
        """
        return group_by_str




