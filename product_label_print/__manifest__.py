# -*- coding: utf-8 -*-
{
    'name': "Print Product Labels",

    'summary': """
        Print Labels of Products""",

    'description': """
        Print Labels of Products
    """,

    'author': "Angstrom Mena",
    'website': "https://www.icq24.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['product'],

    # always loaded
    'data': [
        'reports/report_product_label.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'auto_install': False,
    'application': False,
}
