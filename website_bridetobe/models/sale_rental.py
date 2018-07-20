# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import Warning
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SaleRental(models.Model):
    _name = "sale.rental"
    _inherit = ['sale.rental', 'mail.thread']
    _order = 'delivery_date,state_internal'

    @api.one
    def _get_residual_time(self):
        if self.delivery_date and self.test_date:
            if datetime.today() > datetime.strptime(self.test_date, DEFAULT_SERVER_DATETIME_FORMAT):
                residual_datetime = datetime.strptime(self.delivery_date,
                                                      DEFAULT_SERVER_DATETIME_FORMAT) - datetime.today()
            else:
                residual_datetime = datetime.strptime(self.test_date, DEFAULT_SERVER_DATETIME_FORMAT) - datetime.today()
            residual_time = residual_datetime.total_seconds() // 3600
            residual_datetime.total_seconds() // 3600
            security_rental = self.start_order_id.company_id.security_rental
            if residual_time > security_rental and residual_time < (security_rental * 2) and self.state in (
                    'ordered', 'pending'):
                self.alert_color = "yellow"
            elif residual_time <= security_rental and self.state in ('ordered', 'pending'):
                self.alert_color = "crimson"

        if not self.alert_color:
            self.alert_color = self.state_internal.state_color
        if self.state == 'tested_out':
            self.alert_color = 'yellow'

    @api.model
    def _get_modista_domain(self):
        return [('department_id', '=', self.env.ref('website_bridetobe.modista').id)]

    @api.model
    def _get_default_internal_state(self):
        return self.state_internal.search([('sequence', '=', 1)])

    state_internal = fields.Many2one('sale.rental.internal.state',
                                     string="Estado Interno", ondelete="restrict",
                                     default=_get_default_internal_state)
    modista = fields.Many2one("hr.employee", string="Modista", domain=_get_modista_domain)
    event_place = fields.Char(related="start_order_id.event_place", string="Event Place")
    end_date = fields.Date(store=True)
    state = fields.Selection(selection_add=[('ordered', 'Sin Asignar'),
                                            ('pending', 'Pendiente de Prueba'),
                                            ('tested_out', 'Prueba y Entrega'),
                                            ('tested', 'Probado'),
                                            ('out', 'Entregado')], readonly=False,
                             track_visivility='onchange',
                             )
    alert_color = fields.Char(string="Alert Color",
                              compute="_get_residual_time")
    product_barcode = fields.Char(related="rental_product_id.barcode",
                                  readonly=True)
    delivery_date = fields.Datetime(string="Fecha Entrega")
    test_date = fields.Datetime(string="Fecha Prueba")
    comments = fields.Text(string="Comments")
    details = fields.Text(string="Details")
    rental_product_id = fields.Many2one(
        'product.template', related='',
        string="Vestido", readonly=False, track_visibility="onchange")
    internal_comment = fields.Text(string="Nota Interna", track_visibility='onchange')
    receipt_render = fields.Text()
    receipt_url = fields.Char()
    seller_id = fields.Many2one(related='start_order_id.seller_id', string="Vendedor")
    current_days = fields.Integer(compute="_get_current_days", string="Dias Transcurridos")
    start_date = fields.Date(related='start_order_line_id.start_date', readonly=False, track_visibility="onchange",
                             string="Fecha Evento")

    @api.depends('state')
    def next_state(self):
        if self.state_internal:
            last_state_sequence = max(
                a.sequence for a in self.state_internal.search([('sale_order_state', '=', False)]))
            if last_state_sequence != self.state_internal.sequence:
                next_sequence = min(
                    a.sequence for a in self.state_internal.search(
                        [('sequence', '>', self.state_internal.sequence), ('sale_order_state', '=', False)]))
                self.state_internal = self.state_internal.search([('sequence', '=', next_sequence)])
        else:
            state_ids = [a.sequence for a in self.state_internal.search([])]
            if state_ids:
                first_state = min(a.sequence for a in self.state_internal.search([]))
                self.state_internal = self.state_internal.search([('sequence', '=', first_state)])
            else:
                raise Warning('No existen estados Definidos')

    @api.one
    @api.depends(
        'start_order_line_id', 'extension_order_line_ids.end_date',
        'extension_order_line_ids.state', 'start_order_line_id.end_date')
    def _compute_display_name_field(self):
        self.display_name = u'[%s] %s (%s)' % (
            self.partner_id.name,
            self.rented_product_id.name,
            self._fields['state'].convert_to_export(self.state, self))

    def get_details(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.rental',
            'res_id': self.id,
            'context': self.env.context,
            'view_id': self.env.ref('sale_rental.sale_rental_form').id,
        }

    @api.one
    @api.depends(
        'start_order_line_id.order_id.state',
        'start_order_line_id.procurement_ids.move_ids.state',
        'start_order_line_id.procurement_ids.move_ids.move_dest_id.state',
        'sell_order_line_ids.procurement_ids.move_ids.state',
    )
    def _compute_procurement_and_move(self):
        procurement = False
        in_move = False
        out_move = False
        sell_procurement = False
        sell_move = False
        state = False
        if (self.start_order_line_id and self.start_order_line_id.procurement_ids):
            procurement = self.start_order_line_id.procurement_ids[0]

            if procurement.move_ids:
                for move in procurement.move_ids:
                    if move.move_dest_id:
                        out_move = move
                        in_move = move.move_dest_id
            if (self.sell_order_line_ids and self.sell_order_line_ids[0].procurement_ids):
                sell_procurement = self.sell_order_line_ids[0].procurement_ids[0]
                if sell_procurement.move_ids:
                    sell_move = sell_procurement.move_ids[0]
            state = 'ordered'
            if out_move and in_move:
                if out_move.state == 'done':
                    state = 'out'
                if out_move.state == 'done' and in_move.state == 'done':
                    state = 'in'
                if (out_move.state == 'done' and in_move.state == 'cancel' and sell_procurement):
                    state = 'sell_progress'
                    if sell_move and sell_move.state == 'done':
                        state = 'sold'
            if self.start_order_line_id.order_id.state == 'cancel':
                state = 'cancel'
        self.procurement_id = procurement
        self.in_move_id = in_move
        self.out_move_id = out_move
        self.state = state
        self.sell_procurement_id = sell_procurement
        self.sell_move_id = sell_move
        if self.state == 'in':
            self.rental_product_id = False

    @api.multi
    def write(self, vals):
        rental_product_id = self.rental_product_id.rented_product_id.id
        if vals.get('start_date'):
            self.start_order_line_id.write({'start_date': vals.get('start_date'), 'end_date': vals.get('start_date')})
            self.in_picking_id.min_date = fields.Datetime.from_string(vals.get('start_date'))
            self.out_picking_id.write({'min_date': fields.Datetime.from_string(vals.get('start_date'))})
        sale_rental = super(SaleRental, self).write(vals)
        message_body = False
        delivery_date = ""
        test_date = ""
        self_test_date = ""
        self_delivery_date = ""
        if self.test_date:
            self_test_date = fields.Datetime.from_string(self.test_date) + timedelta(hours=-4)
            test_date = datetime.strftime(self_test_date, '%d/%m/%Y %I:%M %p')

        if self.delivery_date:
            self_delivery_date = fields.Datetime.from_string(self.delivery_date) + timedelta(hours=-4)
            delivery_date = datetime.strftime(fields.Datetime.from_string(self.delivery_date),
                                              '%d/%m/%Y %I:%M %p')
        if vals.get('test_date') or vals.get('delivery_date'):
            if self_delivery_date and self_test_date:
                if self_delivery_date.date() == self_test_date.date():
                    super(SaleRental, self).write({'state': 'tested_out'})
        if self.modista and vals.get('test_date'):
            if not vals.get('state'):
                self.state = 'pending'
            if not vals.get('state_internal'):
                self.state_internal = self.env.ref('website_bridetobe.internal_state_ajuste').id
            if self.state_internal.message_body:
                message_body = self.state_internal.message_body.format(self.partner_id.name,
                                                                       self.rental_product_id.barcode or "",
                                                                       self.state_internal.name,
                                                                       self.modista.name,
                                                                       self.start_order_id.name,
                                                                       test_date,
                                                                       delivery_date)
        elif vals.get('rental_product_id'):
            message_body = "ESTIMADO CLIENTE LE INFORMAMOS QUE SE HA " \
                           "EFECTUANDO UN CAMBIO DE VESTIDO, " \
                           "CODIGO DEL VESTIDO SELECCIONADO " + (self.rental_product_id.barcode or "")

        if message_body:
            self.message_ids.create({
                "subject": "Detalles de su Renta" + self.start_order_id.name,
                "subtype_id": 1,
                "res_id": self.id,
                "partner_ids": [(4, self.partner_id.id)],
                "needaction_partner_ids": [(4, self.partner_id.id)],
                "body": message_body,
                "record_name": self.display_name,
                "date": datetime.today(),
                "model": 'sale.rental',
                "author_id": self.env.user.id,
                "message_type": "email",
                "email_from": self.env.user.email})

        if 'rental_product_id' in vals:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.rental_product_id.id)],
                                                            limit=1)
            for move_line in self.out_picking_id.move_lines:
                if move_line.product_id.product_tmpl_id.id == rental_product_id:
                    move_line.product_id = self.env['product.product'].search(
                        [('product_tmpl_id', '=', product_id.rented_product_id.id)], limit=1)
            for pack_operation in self.out_picking_id.pack_operation_product_ids:
                if pack_operation.product_id.product_tmpl_id.id == rental_product_id:
                    pack_operation.product_id = self.env['product.product'].search(
                        [('product_tmpl_id', '=', product_id.rented_product_id.id)], limit=1)

            for move_line in self.in_picking_id.move_lines:
                if move_line.product_id.product_tmpl_id.id == rental_product_id:
                    move_line.product_id = self.env['product.product'].search(
                        [('product_tmpl_id', '=', product_id.rented_product_id.id)], limit=1)
            for pack_operation in self.in_picking_id.pack_operation_product_ids:
                if pack_operation.product_id.product_tmpl_id.id == rental_product_id:
                    pack_operation.product_id = self.env['product.product'].search(
                        [('product_tmpl_id', '=', product_id.rented_product_id.id)], limit=1)

            self.start_order_line_id.procurement_ids[0].product_id = product_id
            self.start_order_line_id.procurement_ids[0].name = self.rental_product_id.name
            self.start_order_line_id.product_id = product_id
            self.start_order_line_id.name = self.rental_product_id.name
        return sale_rental

    def get_availability(self, rental_product_id=False):
        date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATE_FORMAT)
        date_start = date - timedelta(days=date.weekday())
        date_end = date + timedelta(days=7)
        product_availability = self.env['sale.rental'].sudo().search(
            [('rental_product_id', '=', rental_product_id or self.rental_product_id.id),
             ('start_date', '<=', datetime.strftime(date_end, DEFAULT_SERVER_DATE_FORMAT)),
             ('start_date', '>=', datetime.strftime(date_start, DEFAULT_SERVER_DATE_FORMAT)),
             ('state', '!=', 'cancel')])
        if product_availability:
            raise Warning("Este Articulo no esta disponible en esta Fecha")

    @api.onchange('rental_product_id')
    def onchange_rental_product_id(self):
        self.get_availability()

    def print_receipt(self):
        receipt_url = self.env['ir.values'].get_default('stock.config.settings', 'label_printer_url') or "ZD410"
        # ============================
        self.next_state()
        out_picking_id = self.out_picking_id
        out_picking_id.sudo().force_assign()
        for picking_line in out_picking_id.pack_operation_product_ids:
            product_id = self.env['product.product'].search(
                [('product_tmpl_id', '=', self.rented_product_id.id)])
            if picking_line.product_id.id == product_id.id and picking_line.qty_done == 0:
                picking_line.sudo().write({'qty_done': 1.0})
        # ===============
        receipt_render = """^XA 
				  ^FO0,20^A0N,50,62^FB500,0,0,C^FD{0}^FS 
				  ^FO0,60^A0N,40,40^FB500,1,0,C^FD{2}^FS
				  ^FO30,100^BY4^BCN,100,Y,N,N^FD{1}^FS
				  ^XZ""".format(self.sudo().partner_id.company_id.name.encode('utf-8'),
                                self.start_order_id.name.encode('utf-8'),
                                self.sudo().partner_id.name.encode('utf-8'))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print Label',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'posbox.print',
            'context': {"default_receipt_url": receipt_url,
                        "default_receipt": receipt_render
                        },
            'view_id': self.env.ref('posbox_send.qztry_print_label_form').id,
            'target': 'new',
        }

    def cancel_rental(self):
        if self.out_picking_id.state != 'done':
            self.out_picking_id.action_cancel()
        if self.in_picking_id.state != 'done':
            self.in_picking_id.action_cancel()
        payment_obj = self.env['account.payment']
        self.start_order_id.action_done()
        self.state = 'cancel'
        for invoice_id in self.start_order_id.invoice_ids:
            if invoice_id.state in ('open', 'paid') and invoice_id.type not in (
                    'in_refund', 'out_refund') and not invoice_id.refund_invoice_ids:
                if invoice_id.state in ('open'):
                    payment = payment_obj.create({'invoice_ids': [(4, invoice_id.id)],
                                                  'journal_id': self.env['account.journal'].search(
                                                      [('code', '=', ('PDR'))], limit=1).id,
                                                  'payment_method_id': self.env['account.payment.method'].search(
                                                      [('code', '=', 'electronic')], limit=1).id,
                                                  'amount': invoice_id.residual,
                                                  'payment_type': 'inbound',
                                                  'partner_type': 'customer',
                                                  'communication': 'Pagos Generados por Descuentos y/o Reenvolsos',
                                                  'partner_id': invoice_id.partner_id.id})
                    payment.post()
                refund_id = invoice_id.copy({'type': 'out_refund',
                                             'refund_reason': "Cancelacion de Renta",
                                             'origin_invoice_ids': [(4, invoice_id.id)]})
                if (fields.Datetime.from_string(fields.Date.today()) - fields.Datetime.from_string(
                        invoice_id.date_invoice)).days > 30:
                    for refund_line_id in refund_id.invoice_line_ids:
                        refund_line_id.invoice_line_tax_ids = False

    @api.onchange('delivery_date')
    def onchange_delivery_date(self):
        for rental_id in self:
            if rental_id.out_picking_id:
                rental_id.out_picking_id.min_date = rental_id.delivery_date

    @api.onchange('start_date')
    def onchange_start_date(self):
        self.test_date = False
        self.delivery_date = False

    @api.model
    def create(self, vals):
        start_order_line_id = self.env['sale.order.line'].browse(vals.get('start_order_line_id'))
        start_order_id = self.env['sale.order'].browse(vals.get('start_order_id'))
        vals['rental_product_id'] = start_order_line_id.product_id.product_tmpl_id.id
        vals['comments'] = start_order_id.comments
        return super(SaleRental, self).create(vals)

    @api.multi
    def _get_current_days(self):
        for rental in self:
            rental.current_days = (
                datetime.today() - datetime.strptime(rental.start_date, DEFAULT_SERVER_DATE_FORMAT)).days

    @api.one
    def send_return_email(self):
        self.message_post(
            body="Estimado cliente le solicitamos realizar la devolucion del vestido codigo %s utilizado en fecha de evento %s lo antes posible." % (
                (self.rental_product_id.barcode or self.rental_product_id.default_code), self.start_date),
            message_type='notification',
            subtype='mt_comment',
            partner_ids=[self.partner_id.id])


# @api.onchange('state_internal')
# def change_state_internal(self):
#     if self.state_internal.message_send:
#         try:
#             self.sudo().message_ids.create(
#                 {"subject": "Detalles de su Orden" + self.start_order_id.name,
#                  "subtype_id": 1,
#                  "res_id": self.id,
#                  "partner_ids": [(4, self.partner_id.id)],
#                  "needaction_partner_ids": [(4, self.partner_id.id)],
#                  "body": self.state_internal.message_body.format(self.partner_id.name,
#                                                                  self.rented_product_id.name,
#                                                                  self.state_internal.name,
#                                                                  self.modista.name,
#                                                                  self.start_order_id.name),
#                  "record_name": self.display_name,
#                  "date": datetime.today(),
#                  "model": 'sale.rental',
#                  "author_id": self.env.user.id,
#                  "message_type": "email",
#                  "email_from": self.env.user.email})
#         except (KeyError, IndexError):
#             _logger.error('El cuerpo del mensaje no esta Configurado correctamente')
