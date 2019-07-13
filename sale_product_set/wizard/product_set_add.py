# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api,_
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError

class inagro_sale_order_line_ProductSet(models.Model):
    _inherit = 'sale.order.line'

    product_set_id = fields.Many2one('product.set', string='Package', required=False)

class ProductSetAdd(models.TransientModel):
    _name = 'product.set.add'
    _rec_name = 'product_set_id'
    _description = "Wizard model to add product set into a quotation"

    product_set_id = fields.Many2one(
        'product.set', 'Product set', required=True)
    quantity = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'), required=True,
        default=1)

    @api.multi
    def add_set(self):
        """ Add product set, multiplied by quantity in sale order line """
        so_id = self._context['active_id']
        id_paket = self.product_set_id

        # print(so_id,'so_id')
        # print(id_paket,'id_paket')
        # exit();

        if not so_id:
            return
        so = self.env['sale.order'].browse(so_id)
        max_sequence = 0
        if so.order_line:
            max_sequence = max([line.sequence for line in so.order_line])
        sale_order_line_env = self.env['sale.order.line']
        sale_order_line = self.env['sale.order.line']
        for set_line in self.product_set_id.set_line_ids:
            sale_order_line |= sale_order_line_env.create(
                self.prepare_sale_order_line_data(
                    so_id, set_line,id_paket,
                    max_sequence=max_sequence))
        return sale_order_line

    @api.multi
    def prepare_sale_order_line_data(self, sale_order_id, set_line,id_paket,
                                     max_sequence=0):
        # print(set_line.product_id.id,' product')
        # print(set_line.product_id.name,' product name')
        

        # product_qty = set_line.quantity * self.quantity
        # product = set_line.product_id.id
        # minimum_order_qty = self.env['product.product'].browse(product).minimum_order_quantity 
        # if product_qty < minimum_order_qty: 
        #     raise ValidationError(_('Minimum order quantity of the product ' +set_line.product_id.name+' is ' +str(minimum_order_qty)))

        # print('lanjut')
        # exit()
        self.ensure_one()
        sale_line = self.env['sale.order.line'].new({
            'order_id': sale_order_id,
            'product_id': set_line.product_id.id,
            'product_uom_qty': set_line.quantity * self.quantity,
            'product_uom': set_line.product_id.uom_id.id,
            'sequence': max_sequence + set_line.sequence,
            'product_set_id': id_paket,
        })
        sale_line.product_id_change()
        line_values = sale_line._convert_to_write(sale_line._cache)
        return line_values
