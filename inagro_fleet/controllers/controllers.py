# -*- coding: utf-8 -*-

from collections import OrderedDict

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

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

class PortalFleet(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super(PortalFleet, self)._prepare_portal_layout_values()
        values['contract_count'] = request.env['fleet.vehicle.log.contract'].search_count([])
        return values
    
    def _vehicle_log_contract_get_page_view_values(self, contract, access_token, **kwargs):
        values = {
            'page_name': 'Vehicle Log Contract',
            'contract': contract,
        }
        return self._get_page_view_values(contract, access_token, values, 'my_fleet_log_contract_history', False, **kwargs)
    
    
    @http.route(['/my/fleetlogcontract', '/my/fleetlogcontract/page/<int:page>'], type='http', auth="user", website=True)
    def portal_log_contracts(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        ContractOrder = request.env['fleet.vehicle.log.contract']
        
        domain = []

        archive_groups = self._get_archive_groups('fleet.vehicle.log.contract', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
            
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
            }
        
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['expiration_date']
        
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['futur', 'open', 'diesoon','expired','closed'])]},
            'futur': {'label': _('Incoming'), 'domain': [('state', '=', 'futur')]},
            'open': {'label': _('Open'), 'domain': [('state', '=', 'open')]},
            'diesoon': {'label': _('Expiring Soon'), 'domain': [('state', '=', 'diesoon')]},
            'expired': {'label': _('Expired'), 'domain': [('state', '=', 'expired')]},
            'closed': {'label': _('Closed'), 'domain': [('state', '=', 'closed')]},
            }
    
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        
        # count for pager
        contract_count = ContractOrder.search_count(domain)
        
        # make pager
        pager = portal_pager(
            url="/my/fleetlogcontract",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=contract_count,
            page=page,
            step=self._items_per_page
        )
        
        # search the purchase orders to display, according to the pager data
        orders = ContractOrder.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_fleet_log_contract_history'] = orders.ids[:100]
        
        values.update({
            'date': date_begin,
            'orders': orders,
            'page_name': 'contract',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': '/my/fleetlogcontract',
        })
        return request.render("inagro_fleet.portal_log_contracts", values)
        
        
    @http.route(['/my/fleetlogcontract/<int:contract_id>'], type='http', auth="public", website=True)
    def portal_log_contract(self, contract_id=None, access_token=None, **kw):
        try:
            contract_sudo = self._document_check_access('fleet.vehicle.log.contract', contract_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._vehicle_log_contract_get_page_view_values(contract_sudo, access_token, **kw)
        return request.render("inagro_fleet.portal_log_contract", values)