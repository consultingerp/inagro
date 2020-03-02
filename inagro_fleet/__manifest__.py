# -*- coding: utf-8 -*-
{
    'name': "inagro_fleet",

    'summary': """
        rayci232@gmail.com""",

    'description': """
        -
    """,

    'author': "INAGRO",
    'website': "https://www.inagro.co.id/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','hr'],

    # always loaded
    'data': [
        'data/v_req_seq.xml',
        'security/ir.model.access.csv',
        'security/group.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu_item.xml',
        'views/vehicle_request.xml',
        'views/inherit_contract.xml',
#         'views/inherit_company.xml',
        'report/schedule_view.xml',
        'report/contract_report_views.xml',
        'report/contract_vehicle.xml',
        'views/portal_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}