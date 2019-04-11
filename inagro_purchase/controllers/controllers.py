# -*- coding: utf-8 -*-
from odoo import http

# class InagroPurchase(http.Controller):
#     @http.route('/inagro_purchase/inagro_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_purchase/inagro_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_purchase.listing', {
#             'root': '/inagro_purchase/inagro_purchase',
#             'objects': http.request.env['inagro_purchase.inagro_purchase'].search([]),
#         })

#     @http.route('/inagro_purchase/inagro_purchase/objects/<model("inagro_purchase.inagro_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_purchase.object', {
#             'object': obj
#         })