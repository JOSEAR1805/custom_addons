from odoo import models, fields, api
import json


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    event_date = fields.Date(string="Fecha Evento")
    seller_id = fields.Many2one('hr.employee', string="Vendedor")

    def _payment_is_inside(self, dict, journal_name, amount):
        for obj in dict:
            if obj['journal_name'] == journal_name:
                obj['amount'] += amount
                return True
        return False

    @api.one
    def get_payments(self):
        payment_ids = []
        if self.payments_widget:
            for obj in json.loads(self.payments_widget)['content']:
                if not self._payment_is_inside(payment_ids, obj.get('journal_name'), obj.get('amount')):
                    payment_ids.append({'journal_name': obj.get('journal_name'),
                                        'amount': obj.get('amount')})
            return payment_ids
        else:
            return False

    def ntw(self, number, option, option2):
        return num2words(number, ordinal=option2, lang=option)

    def print_receipt(self):
        return self.env['posbox.print'].posbox_send_ticket('website_bridetobe.report_account_invoice_ticket',
                                                    {'invoice': self, 'company': self.company_id})