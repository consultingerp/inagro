# -*- coding: utf-8 -*-
{
    'name': "Inagro Hotel",

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
    'depends': ['hotel','hotel_reservation'],

    # always loaded
    'data': [
        'security/hotel_group.xml',
        'security/ir.model.access.csv',
        'views/hotel_view.xml',
        'report/reservation_room_view.xml',
        'report/info_booking.xml',
        'report/folio_report.xml',
        'report/folio_report_template.xml',
        'views/reservasi.xml',
        'views/hotel_folio_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}