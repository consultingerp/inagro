# -*- coding: utf-8 -*-
{
    'name': "Inagro User To Inventory",

    'summary': """
        rayci232@gmail.com""",

    'description': """
        Modul untuk mengatur role akses user pada dashboard inventory
    """,

    'author': "INAGRO",
    'website': "https://www.inagro.co.id/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/inherit_res_user.xml',
        'views/inherit_stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}