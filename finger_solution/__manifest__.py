# -*- coding: utf-8 -*-
{
    'name' : 'fingerprint Solution',
    'version' : '0.1',
    'summary': '',
    'sequence': 30,
    'author': "RPJ / rayci232@gmail.com",
    'website': "http://www.kadai.prahasiber.com",
    'description': """
        Attendance with fingerprint
    """,
    'category': 'Human resource',
    'depends' : ['hr_attendance'],
    'data': [
        'views/hr_employee.xml',
        'views/attendance_log.xml',
        'views/inherit_attendance.xml',

        'data/download_data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
