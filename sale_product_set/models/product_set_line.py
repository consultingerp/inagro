# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api,fields, models
from odoo.addons import decimal_precision as dp


class ProductSetLine(models.Model):
    _name = 'product.set.line'
    _description = 'Product set line'
    _rec_name = 'product_id'
    _order = 'sequence'

    product_id = fields.Many2one(
        comodel_name='product.product',
        domain=[('sale_ok', '=', True)],
        string='Product',
        required=True
    )
    quantity = fields.Float(
        string='Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        required=True,
        default=1
    )
    product_set_id = fields.Many2one(
        'product.set',
        string='Set',
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        required=True,
        default=0,
    )

    list_price = fields.Float(
        'Sales Price', default=1.0,store=True,
        digits=dp.get_precision('Product Price'),related="product_id.list_price")

    total_price = fields.Float(
        'Total Price', default=1.0,
        digits=dp.get_precision('Total Price'))

    @api.onchange('quantity','list_price')
    def _total_price(self):
        self.total_price = self.quantity * self.list_price
