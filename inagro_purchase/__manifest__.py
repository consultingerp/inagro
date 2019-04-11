# -*- coding: utf-8 -*-
{
    'name': "Inagro Purchase Module",

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
    # 'images': ['static/description/logo.jpg'],
    'depends': ['base','purchase','purchase_stock','sprogroup_purchase_request','hr'],

    # always loaded
    'data': [
        'data/filter_dir.xml',
        'data/bis_type.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/inherit_purchase_request.xml',
        'views/inherit_purchase_order.xml',
        'views/inherit_department.xml',
        'views/bis_type.xml',

        'report/purchase.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}