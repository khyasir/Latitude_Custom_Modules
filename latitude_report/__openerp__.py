# -*- coding: utf-8 -*-
{
    'name': "latitude_report",

    'summary': """
        Sale Tax Invoice of Latitude""",

    'description': """
        Sale Tax Invoice of Latitude
    """,

    'author': "Ali",
    'website': "http://oxenlab.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'latitude_report_define.xml',
        'latitude_report.xml',
    ],
    'images': ['static/icon/icon.png'],
    # 'css': ['static/css/report.css'],
}