# -*- coding: utf-8 -*-
from odoo import http

# class InagroSales(http.Controller):
#     @http.route('/inagro_sales/inagro_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_sales/inagro_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_sales.listing', {
#             'root': '/inagro_sales/inagro_sales',
#             'objects': http.request.env['inagro_sales.inagro_sales'].search([]),
#         })

#     @http.route('/inagro_sales/inagro_sales/objects/<model("inagro_sales.inagro_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_sales.object', {
#             'object': obj
#         })