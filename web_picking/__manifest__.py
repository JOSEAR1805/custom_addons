# -*- coding: utf-8 -*-
{
    'name': 'Web Picking',
    'category': 'website',
    'sequence': 50,
    'summary': 'Web Picking',
    'website': 'https://www.icq24.com',
    'author': 'Angstrom Mena',
    'version': '1.0',
    'description': """
Web Pciking Manager
=======================
        """,
    'depends': ['stock','website','sale', 'account'],
    'installable': True,
    'data': [
        'views/web_picking_list.xml',
        'views/web_picking_details.xml',
        'views/web_picking_signature.xml',
    ],
    'application': False,
}
