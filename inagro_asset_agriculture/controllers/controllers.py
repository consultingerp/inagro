# -*- coding: utf-8 -*-
from odoo import http

# class InagroAssetAgriculture(http.Controller):
#     @http.route('/inagro_asset_agriculture/inagro_asset_agriculture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_asset_agriculture/inagro_asset_agriculture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_asset_agriculture.listing', {
#             'root': '/inagro_asset_agriculture/inagro_asset_agriculture',
#             'objects': http.request.env['inagro_asset_agriculture.inagro_asset_agriculture'].search([]),
#         })

#     @http.route('/inagro_asset_agriculture/inagro_asset_agriculture/objects/<model("inagro_asset_agriculture.inagro_asset_agriculture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_asset_agriculture.object', {
#             'object': obj
#         })