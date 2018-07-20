from odoo import models, fields, api

class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    security_rental = fields.Integer(related='company_id.security_rental')

    # @api.multi
    # def set_deposit_product_id_defaults(self):
    #     return self.env['ir.values'].sudo().set_default(
    #         'sale.config.settings', 'deposit_product_id_setting', self.deposit_product_id_setting.id)