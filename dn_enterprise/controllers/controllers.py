# -*- coding: utf-8 -*-
from odoo import http

# class DnEnterprise(http.Controller):
#     @http.route('/dn_enterprise/dn_enterprise/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_enterprise/dn_enterprise/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_enterprise.listing', {
#             'root': '/dn_enterprise/dn_enterprise',
#             'objects': http.request.env['dn_enterprise.dn_enterprise'].search([]),
#         })

#     @http.route('/dn_enterprise/dn_enterprise/objects/<model("dn_enterprise.dn_enterprise"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_enterprise.object', {
#             'object': obj
#         })