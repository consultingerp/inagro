

from odoo import api, fields, models, tools
from odoo.addons import decimal_precision as dp

class inagro_agri_activity_report(models.Model):
    _name = "report.cultivation"
    _description = "Harvest Real Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    crop_location = fields.Char('Crop Location', readonly=True)
    name_varieties = fields.Char('Crop Varieties', readonly=True)
    crop_category = fields.Char('Crop Category', readonly=True)
    product_name = fields.Char('Product', readonly=True)
    product_uom_qty = fields.Float('Qty', digits=dp.get_precision('Product Unit of Measure'), readonly=True)
    name_uom = fields.Char('UOM', readonly=True)
    reference = fields.Char('Reference', readonly=True)
    surce_location = fields.Char('From', readonly=True)
    dest_location = fields.Char('To', readonly=True)
    date_move = fields.Datetime('Date', readonly=True)


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
                min(sm.id) as id,
                area_loc. NAME AS crop_location,
                varieties. NAME AS name_varieties,
                category. NAME AS crop_category,
                sm. NAME as product_name,
                sm.product_uom_qty,
                uom. NAME AS name_uom,
                sm.reference,
                concat (
                    parent_from. NAME,
                    '/',
                    sl_from. NAME
                ) AS surce_location,
                sl_to. NAME AS dest_location,
                sm. DATE as date_move
        """
        return select_str

    def _from(self):
        from_str = """ 
            (
                SELECT
                    *
                FROM
                    stock_move
                WHERE
                    is_cultivation = 't'
                    and state = 'done'
            ) sm
            LEFT JOIN stock_location sl_from ON sm.location_id = sl_from. ID
            LEFT JOIN stock_location sl_to ON sm.location_dest_id = sl_to. ID
            LEFT JOIN stock_location parent_from ON sl_from.location_id = parent_from. ID
            LEFT JOIN uom_uom uom ON sm.product_uom = uom. ID
            LEFT JOIN farmer_location_crops crop ON sm.crop_id = crop. ID
            LEFT JOIN crop_varieties varieties ON sm.varieties_id = varieties. ID
            LEFT JOIN crop_category category ON varieties.category = category. ID
            LEFT JOIN res_partner area_loc ON sm.area_location_id = area_loc. ID
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                category. NAME,
                varieties. NAME,
                area_loc. NAME,
                sm. NAME,
                sm.product_uom_qty,
                uom. NAME,
                sm.reference,
                sl_from. NAME,
                parent_from. NAME,
                sl_to. NAME,
                sm. DATE
        """
        return group_by_str




