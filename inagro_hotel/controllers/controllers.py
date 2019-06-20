# -*- coding: utf-8 -*-
from odoo import http

# class InagroHotel(http.Controller):
#     @http.route('/inagro_hotel/inagro_hotel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_hotel/inagro_hotel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_hotel.listing', {
#             'root': '/inagro_hotel/inagro_hotel',
#             'objects': http.request.env['inagro_hotel.inagro_hotel'].search([]),
#         })

#     @http.route('/inagro_hotel/inagro_hotel/objects/<model("inagro_hotel.inagro_hotel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_hotel.object', {
#             'object': obj
#         })