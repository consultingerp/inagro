# -*- coding: utf-8 -*-
from odoo import http

# class InagroBudget(http.Controller):
#     @http.route('/inagro_budget/inagro_budget/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inagro_budget/inagro_budget/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inagro_budget.listing', {
#             'root': '/inagro_budget/inagro_budget',
#             'objects': http.request.env['inagro_budget.inagro_budget'].search([]),
#         })

#     @http.route('/inagro_budget/inagro_budget/objects/<model("inagro_budget.inagro_budget"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inagro_budget.object', {
#             'object': obj
#         })