# -*- coding: utf-8 -*-
from odoo import http

# class InagroPointOfSale(http.Controller):
#     @http.route('/inagro_point_of_sale/inagro_point_of_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_point_of_sale/inagro_point_of_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_point_of_sale.listing', {
#             'root': '/inagro_point_of_sale/inagro_point_of_sale',
#             'objects': http.request.env['inagro_point_of_sale.inagro_point_of_sale'].search([]),
#         })

#     @http.route('/inagro_point_of_sale/inagro_point_of_sale/objects/<model("inagro_point_of_sale.inagro_point_of_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_point_of_sale.object', {
#             'object': obj
#         })