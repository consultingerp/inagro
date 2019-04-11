# -*- coding: utf-8 -*-
from odoo import http

# class InagroUserInventory(http.Controller):
#     @http.route('/inagro_user_inventory/inagro_user_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_user_inventory/inagro_user_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_user_inventory.listing', {
#             'root': '/inagro_user_inventory/inagro_user_inventory',
#             'objects': http.request.env['inagro_user_inventory.inagro_user_inventory'].search([]),
#         })

#     @http.route('/inagro_user_inventory/inagro_user_inventory/objects/<model("inagro_user_inventory.inagro_user_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_user_inventory.object', {
#             'object': obj
#         })