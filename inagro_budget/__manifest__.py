# -*- coding: utf-8 -*-
{
    'name': "Inagro Budget",

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
    'depends': ['base','inagro_purchase','account_budget'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/rule.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/inherit_budgetary_position.xml',
        'views/inherit_analytic_account.xml',
        'views/menu_budget.xml',
        'views/inherit_budget.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}