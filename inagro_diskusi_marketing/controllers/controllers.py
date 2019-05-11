# -*- coding: utf-8 -*-
from odoo import http

# class InagroDiskusiMarketing(http.Controller):
#     @http.route('/inagro_diskusi_marketing/inagro_diskusi_marketing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_diskusi_marketing/inagro_diskusi_marketing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_diskusi_marketing.listing', {
#             'root': '/inagro_diskusi_marketing/inagro_diskusi_marketing',
#             'objects': http.request.env['inagro_diskusi_marketing.inagro_diskusi_marketing'].search([]),
#         })

#     @http.route('/inagro_diskusi_marketing/inagro_diskusi_marketing/objects/<model("inagro_diskusi_marketing.inagro_diskusi_marketing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_diskusi_marketing.object', {
#             'object': obj
#         })