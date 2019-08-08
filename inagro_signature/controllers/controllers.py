# -*- coding: utf-8 -*-
from odoo import http

# class InagroSignature(http.Controller):
#     @http.route('/inagro_signature/inagro_signature/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_signature/inagro_signature/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_signature.listing', {
#             'root': '/inagro_signature/inagro_signature',
#             'objects': http.request.env['inagro_signature.inagro_signature'].search([]),
#         })

#     @http.route('/inagro_signature/inagro_signature/objects/<model("inagro_signature.inagro_signature"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_signature.object', {
#             'object': obj
#         })