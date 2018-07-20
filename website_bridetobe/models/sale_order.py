# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_modista_domain(self):
        return [('department_id', '=', self.env.ref('website_bridetobe.confecciones').id)]

    def _get_default_internal_state(self):
        first_state = min((a.sequence for a in self.state_internal.search([])) or [0])
        return self.state_internal.search([('sequence', '=', 1)])

    modista = fields.Many2one("hr.employee", string="Modista", domain=_get_modista_domain)
    busto = fields.Float(string="Busto")
    cintura = fields.Float(string="Cintura")
    cadera = fields.Float(string="Cadera")
    event_place = fields.Char(string="Event Place")
    event_date = fields.Date(string="Event Date")
    state_internal = fields.Many2one('sale.rental.internal.state',
                                     string="Internal State",
                                     default=_get_default_internal_state)
    comments = fields.Text(string="Comments")
    falda = fields.Float(string="Largo de Falda")
    details = fields.Text(string="Details")
    seller_id = fields.Many2one('hr.employee', string="Vendedor")

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create()
        invoice_ids = self.env['account.invoice'].browse(res)
        for invoice_id in invoice_ids:
            invoice_id.event_date = self.event_date
            invoice_id.seller_id = self.seller_id
        for order in self:
            for line in order.order_line:
                if line.rental_type == 'new_rental':
                    line.product_id.is_rented = True
        return res

    @api.one
    def send_message(self):
        state_internal = self.state_internal.search([('sale_order_state', '=', self.state)])
        if state_internal.message_send:
            self.state_internal = state_internal
            try:
                self.message_ids.sudo().create({"subject": "Detalles de su Orden No." + self.name,
                                                "subtype_id": 1,
                                                "res_id": self.id,
                                                "partner_ids": [(4, self.partner_id.id)],
                                                "needaction_partner_ids": [(4, self.partner_id.id)],
                                                "body": str(self.state_internal.message_body).format(
                                                    self.partner_id.name,
                                                    "",
                                                    self.state_internal.name,
                                                    self.modista.name,
                                                    self.name),
                                                "record_name": self.name,
                                                "date": datetime.today(),
                                                "model": 'sale.order',
                                                "author_id": self.env.user.id,
                                                "message_type": "email",
                                                "email_from": self.env.user.email})
            except (KeyError, IndexError):
                _logger.error('El cuerpo del mensaje no esta Configurado correctamente')

    @api.multi
    def write(self, vals):
        sale_order = super(SaleOrder, self).write(vals)
        if vals.get('state'):
            self.send_message()
        return sale_order

    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        if vals.get('state'):
            sale_order.send_message()
        return sale_order
