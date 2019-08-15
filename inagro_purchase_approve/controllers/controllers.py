# -*- coding: utf-8 -*-
from odoo import http

# class InagroPurchaseApprove(http.Controller):
#     @http.route('/inagro_purchase_approve/inagro_purchase_approve/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_purchase_approve/inagro_purchase_approve/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_purchase_approve.listing', {
#             'root': '/inagro_purchase_approve/inagro_purchase_approve',
#             'objects': http.request.env['inagro_purchase_approve.inagro_purchase_approve'].search([]),
#         })

#     @http.route('/inagro_purchase_approve/inagro_purchase_approve/objects/<model("inagro_purchase_approve.inagro_purchase_approve"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_purchase_approve.object', {
#             'object': obj
#         })