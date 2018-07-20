from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(string="Codigo de Cliente", help="Codigo de Cliente")