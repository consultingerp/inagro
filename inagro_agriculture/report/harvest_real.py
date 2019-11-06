

from odoo import api, fields, models, tools
from odoo.addons import decimal_precision as dp

class inagro_agri_activity_report(models.Model):
    _name = "report.harvest_real"
    _description = "Harvest Real Report"
    _auto = False
    # _order = 'date_order desc, price_total desc'

    name_crop = fields.Char('Crop Name', readonly=True)
    crop_category = fields.Char('Crop Category', readonly=True)
    name_varieties = fields.Char('Crop Varieties', readonly=True) 
    crop_location = fields.Char('Crop Location', readonly=True)
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
                crop. NAME AS name_crop,
                category. NAME AS crop_category,
                varieties. NAME AS name_varieties,
                area_loc. NAME AS crop_location,
                sm. NAME as product_name,
                sm.product_uom_qty,
                uom. NAME AS name_uom,
                sm.reference,
                sl_from. NAME AS surce_location,
                concat (
                    parent_to. NAME,
                    '/',
                    sl_to. NAME
                ) AS dest_location,
                sm. DATE as date_move
        """
        return select_str

    def _from(self):
        from_str = """ 
            (
                select * from stock_move WHERE is_harvest = 't' and state = 'done'
            ) sm
            LEFT JOIN stock_location sl_from on sm.location_id = sl_from.id
            LEFT JOIN stock_location sl_to on sm.location_dest_id = sl_to.id
            LEFT JOIN stock_location parent_to on sl_to.location_id = parent_to.id
            LEFT JOIN uom_uom uom on sm.product_uom= uom.id
            LEFT JOIN farmer_location_crops crop on sm.crop_id = crop.id
            LEFT JOIN crop_category category on crop.category_id = category.id
            LEFT JOIN crop_varieties varieties on crop.varieties_id = varieties.id
            LEFT JOIN res_partner area_loc on crop.area_location_id = area_loc.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                crop. NAME,
                category. NAME,
                varieties. NAME,
                area_loc. NAME,
                sm. NAME,
                sm.product_uom_qty,
                uom. NAME,
                sm.reference,
                sl_from. NAME,
                parent_to. NAME,
                sl_to. NAME,
                sm. DATE
        """
        return group_by_str




