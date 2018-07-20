{
    "name": "Posbox Send",
    "category": '',
    "summary": """
        General
        Permite imprimir en el POSBOX fuera del modulo de POS
       """,
    "sequence": 1,
    'author': "Angstrom Mena",
    'website': "http://www.icq24.com",
    'version': '0.1',

    "depends": ['base'],
    "data": [
        'views/posbox_send_view.xml',
        'views/posbox_print_test.xml',
        'views/web_assets.xml',
    ],

    "installable": True,
    "application": False,
    "auto_install": False,
}