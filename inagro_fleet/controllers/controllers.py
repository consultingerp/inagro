# -*- coding: utf-8 -*-
from odoo import http

# class InagroFleet(http.Controller):
#     @http.route('/inagro_fleet/inagro_fleet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_fleet/inagro_fleet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_fleet.listing', {
#             'root': '/inagro_fleet/inagro_fleet',
#             'objects': http.request.env['inagro_fleet.inagro_fleet'].search([]),
#         })

#     @http.route('/inagro_fleet/inagro_fleet/objects/<model("inagro_fleet.inagro_fleet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_fleet.object', {
#             'object': obj
#         })