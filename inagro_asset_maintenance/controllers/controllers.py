# -*- coding: utf-8 -*-
from odoo import http

# class InagroAssetMaintenance(http.Controller):
#     @http.route('/inagro_asset_maintenance/inagro_asset_maintenance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_asset_maintenance/inagro_asset_maintenance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_asset_maintenance.listing', {
#             'root': '/inagro_asset_maintenance/inagro_asset_maintenance',
#             'objects': http.request.env['inagro_asset_maintenance.inagro_asset_maintenance'].search([]),
#         })

#     @http.route('/inagro_asset_maintenance/inagro_asset_maintenance/objects/<model("inagro_asset_maintenance.inagro_asset_maintenance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_asset_maintenance.object', {
#             'object': obj
#         })