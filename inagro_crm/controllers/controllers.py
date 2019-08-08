# -*- coding: utf-8 -*-
from odoo import http

# class InagroCrm(http.Controller):
#     @http.route('/inagro_crm/inagro_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_crm/inagro_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_crm.listing', {
#             'root': '/inagro_crm/inagro_crm',
#             'objects': http.request.env['inagro_crm.inagro_crm'].search([]),
#         })

#     @http.route('/inagro_crm/inagro_crm/objects/<model("inagro_crm.inagro_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_crm.object', {
#             'object': obj
#         })