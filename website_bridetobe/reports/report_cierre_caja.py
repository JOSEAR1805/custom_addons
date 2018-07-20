from odoo import models, api, _, fields
from odoo.exceptions import UserError


class ReportCierreCaja(models.TransientModel):
    _name = 'report.bridetobe.cierre_caja'

    date = fields.Date(string="Dia", required=True)

    def get_payments(self):
        payments = []
        payment_ids = self.env['account.payment'].search([('payment_date', '=', self.date),
                                                          ('payment_type', '=', 'inbound'),
                                                          ('state','!=','draft')])
        for payment_id in payment_ids:
            payment_type = ""
            transfer_type = ""
            if 'TCR' in payment_id.journal_id.code:
                payment_type = 'tarjeta'
            elif 'TB' in payment_id.journal_id.code:
                payment_type = 'transferencia'
                transfer_type = payment_id.journal_id.code
            elif 'CSH' in payment_id.journal_id.code:
                payment_type = 'efectivo'
            elif 'CHE' in payment_id.journal_id.code:
                payment_type = 'cheque'
            else:
                payment_type = 'otros'
            payments.append({
                'date': payment_id.payment_date,
                'partner': payment_id.partner_id.name,
                payment_type: payment_id.amount,
                'transfer_type': transfer_type,
                'invoice': payment_id.communication
            })
        return payments

    def _print_report(self, data):
        raise UserError(_('Not implemented.'))

    @api.multi
    def check_report(self):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'website_bridetobe.cierre_caja',
        }
        # for payment_id in self.get_payments():
        #     print payment_id.get('efectivo', 'Otro')
        #     # print payment_id.payment_date
        #     # print payment_id.partner_id.name
        #     # print payment_id.amount
        #     # if 'TCR' in payment_id.journal_id.code:
        #     #     print 'Tarjeta'
        #     # elif 'TB' in payment_id.journal_id.code:
        #     #     print 'Transaccion'
        #     # elif 'CSH' in payment_id.journal_id.code:
        #     #     print 'Efectivo'
        #     # print payment_id.journal_id.name
        #     # print payment_id.communication
        #     print "===================================="
