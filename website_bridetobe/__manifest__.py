# -*- coding: utf-8 -*-
{
    'name': 'Website Bridetobe',
    'category': 'bridetobe',
    'sequence': 50,
    'summary': 'Website Updates for Bridetobe',
    'website': 'https://www.icq24.com',
    'author': 'Angstrom Mena',
    'version': '1.0',
    'description': """
ICQ24 Website Bridetobe
=======================
        """,
    'depends': ['sale_rental',
                'website',
                'hr',
                'ncf_manager',
                'sale',
                'sales_team',
                'base',
                'sale_stock',
                'web_quote',
                'posbox_send',
                'contacts'
                ],
    'installable': True,
    'data': [
        "security/sales_bridetobe_security.xml",
        "security/ir.model.access.csv",
        "wizards/sale_rental_cancel_wizard_view.xml",
        "wizards/process_unpaid_delivery_view.xml",
        "data/hr_department.xml",
        "data/default_internal_state.xml",
        "data/ir_sequence_data.xml",
        "data/default_products.xml",
        "data/default_payments.xml",
        "views/website_templates.xml",
        "views/website_confecciones_template.xml",
        "views/hr_employee.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "reports/pos_invoice.xml",
        "views/sale_rental.xml",
        "views/product_template.xml",
        "views/sale_rental_internal_state.xml",
        "views/stock_picking_view.xml",
        "views/view_sales_config.xml",
        "views/account_invoice_view.xml",
        "views/res_company_view.xml",
        "views/confecciones_view.xml",
        "reports/report_product_label.xml",
        "reports/report_ficha_trabajo_modista.xml",
        "reports/report_ticket_entrega.xml",
        "reports/pos_invoice.xml",
        "reports/payment_receipt.xml",
        "reports/report_account_invoice_ticket.xml",
        "reports/report_cierre_caja.xml",
        "reports/report_ticket_recepcion.xml",
        "reports/report_invoice.xml",
        "views/menu_items.xml",
        "views/quote_views_inherit.xml",
        "views/stock_config_settings_view.xml",
    ],
    'application': False,
}