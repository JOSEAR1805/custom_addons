from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    comments = fields.Text(string='Observaciones')
    picking_type_code = fields.Selection(related='picking_type_id.code')

    @api.one
    def _compute_amount_due(self):
        invoice_ids = self.env['account.invoice'].search([('origin','=',self.origin)])
        amount_due_total = 0.0
        invoiced = True
        for invoice_id in invoice_ids:
            amount_due_total += invoice_id.residual
            if invoice_id.state == 'draft':
                invoiced = False
        self.amount_due = amount_due_total
        # self.invoiced = invoiced

    @api.one
    def _get_product_barcodes(self):
        product_barcodes = ''
        related_order = self.env['sale.order'].search([('name','=',self.origin)])
        sale_rental_ids = self.env['sale.rental'].search([('start_order_id','=',related_order.id), '|', ('out_picking_id','=',self.id), ('in_picking_id','=',self.id)])
        for sale_rental in sale_rental_ids:
            product_barcodes += str(sale_rental.rental_product_id.barcode or "")
        self.product_barcodes = product_barcodes

    amount_due = fields.Float(string="Pendiente de Pago", compute="_compute_amount_due")
    product_barcodes = fields.Char(compute="_get_product_barcodes", search="_search_product_barcodes")
    # invoiced = fields.Boolean(string="Facturado", compute="_compute_amount_due", store=True)
    invoiced = fields.Boolean(string="Facturado")

    @api.multi
    def action_view_invoice(self):
        invoices = self.env['account.invoice'].search([('origin','=',self.origin)])
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def _search_product_barcodes(self, operator, value):
        stock_picking_ids = self.search([])
        filter_picking_ids = []
        for stock_picking_id in stock_picking_ids:
            for move_product_ids in stock_picking_id.move_lines:
                for rental_service_id in move_product_ids.product_id.rental_service_ids:
                    if rental_service_id.barcode and value in rental_service_id.barcode:
                        filter_picking_ids.append(stock_picking_id.id)
        return [('id', 'in', filter_picking_ids)]

    # def do_new_transfer(self):
    #     if self.amount_due:
    #        raise UserError("Existe un Monto Pendiente de pago por un valor de "+ str(self.amount_due)+" debe procesar el pago antes de continuar la Recepcion")
    #     else:
    #         return super(StockPicking, self).do_new_transfer()

    def process_transfer(self):
        if self.picking_type_code == 'outgoing':
            if self.amount_due:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Procesar Entrega',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.picking.process',
                    'view_id': self.env.ref('website_bridetobe.stock_picking_process_wizard_form').id,
                    'target': 'new',
                }
            else:
                return super(StockPicking, self).do_new_transfer()
        elif self.picking_type_code == 'incoming':
            if self.amount_due:
               raise UserError("Existe un Monto Pendiente de pago por un valor de "+ str(self.amount_due)+" debe procesar el pago antes de continuar la Recepcion")
            else:
                return super(StockPicking, self).do_new_transfer()

    def print_ticket(self):
        if self.picking_type_code == 'incoming':
            return self.env['posbox.print'].posbox_send_ticket('website_bridetobe.report_ticket_recepcion',
                                                        {'receipt': self, 'company': self.company_id})

