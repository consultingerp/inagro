# -*- coding: utf-8 -*-
from odoo import http

# class InagroInvoice(http.Controller):
#     @http.route('/inagro_invoice/inagro_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_invoice/inagro_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_invoice.listing', {
#             'root': '/inagro_invoice/inagro_invoice',
#             'objects': http.request.env['inagro_invoice.inagro_invoice'].search([]),
#         })

#     @http.route('/inagro_invoice/inagro_invoice/objects/<model("inagro_invoice.inagro_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_invoice.object', {
#             'object': obj
#         })