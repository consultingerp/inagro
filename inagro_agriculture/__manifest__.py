# -*- coding: utf-8 -*-
{
    'name': "Inagro Agriculture",

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
    'depends': ['base','odoo_agriculture','product','stock','account'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu_item.xml',
        'views/crop_varieties.xml',
        'views/inherit_crops.xml',
        'views/crop_activity.xml',
        'views/harvest_plan.xml',
        'views/stock_picking.xml',
        'views/stock_picking_type.xml',
        'views/res_partner.xml',
        'report/activity.xml',
        # 'report/stock_move.xml',
        'report/harvest_plan_report.xml',
        'report/harvest_real_report.xml',
        'report/cultivation_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}