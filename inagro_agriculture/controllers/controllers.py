# -*- coding: utf-8 -*-
from odoo import http

# class InagroAgriculture(http.Controller):
#     @http.route('/inagro_agriculture/inagro_agriculture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_agriculture/inagro_agriculture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_agriculture.listing', {
#             'root': '/inagro_agriculture/inagro_agriculture',
#             'objects': http.request.env['inagro_agriculture.inagro_agriculture'].search([]),
#         })

#     @http.route('/inagro_agriculture/inagro_agriculture/objects/<model("inagro_agriculture.inagro_agriculture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_agriculture.object', {
#             'object': obj
#         })