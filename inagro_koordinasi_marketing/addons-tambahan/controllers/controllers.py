# -*- coding: utf-8 -*-
from odoo import http

# class Addons-tambahan(http.Controller):
#     @http.route('/addons-tambahan/addons-tambahan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addons-tambahan/addons-tambahan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addons-tambahan.listing', {
#             'root': '/addons-tambahan/addons-tambahan',
#             'objects': http.request.env['addons-tambahan.addons-tambahan'].search([]),
#         })

#     @http.route('/addons-tambahan/addons-tambahan/objects/<model("addons-tambahan.addons-tambahan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addons-tambahan.object', {
#             'object': obj
#         })