# -*- coding: utf-8 -*-
{
    'name': "vestidores",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jose Artigas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'web_quote',
                'website',
                'website_bridetobe'
    ],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/view_vestidores.xml',
        'views/website_main.xml',
        'views/website_modista.xml',
        'views/website_partner.xml',
        'views/website_queue_making.xml',
        'views/website_queue_test.xml',
        'views/website_queue_tv.xml',
        'views/website_quotes.xml',
        'views/website_vestidores.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}