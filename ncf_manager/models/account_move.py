# -*- coding: utf-8 -*-
###############################################################################
#  Copyright (c) 2015 - Marcos Organizador de Negocios SRL.
#  (<https://marcos.do/>)
#  Write by Eneldo Serrata (eneldo@marcos.do)
#  See LICENSE file for full copyright and licensing details.
#
# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used
# (nobody can redistribute (or sell) your module once they have bought it,
# unless you gave them your consent)
# if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without
# copying any source code or material from the Software. You may distribute
# those modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Softwar or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

from openerp import models, api, fields
from openerp.exceptions import ValidationError
import openerp.addons.decimal_precision as dp


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def post(self):
        invoice = self._context.get('invoice', False)
        if invoice:

            if invoice.amount_total == 0:
                raise ValidationError(
                    u"¡No puede grabar una factura con valor 0!")
            if invoice.type == "out_invoice":
                msg = ""
                if invoice.journal_id.credit_out_invoice is False:
                    invoice.payment_term_id = 1
                    invoice.date_due = fields.Date.today()
                else:
                    if (invoice.overdue_type == "overlimit_overdue" and
                       self.env.user.id != 1):
                        msg = u"El cliente {} no tiene crédito disponible y"
                        " facturas vencidas".format(invoice.partner_id.name)
                    elif (invoice.overdue_type == "overlimit" and
                          self.env.user.id != 1):
                        msg = (u"El cliente {} no tiene crédito disponible"
                               .format(invoice.partner_id.name))
                    elif (invoice.overdue_type == "overdue" and
                          self.env.user.id != 1):
                        msg = (u"El cliente {} tiene facturas vencidas"
                               .format(invoice.partner_id.name))

                    if msg and invoice.authorize is False:
                        raise ValidationError(msg)

            if invoice.type in ('out_invoice', 'out_refund'):
                fiscal_position = invoice.fiscal_position_id.client_fiscal_type
                ncf_control = invoice.journal_id.ncf_control

                if fiscal_position is not False and ncf_control is True:
                    if (fiscal_position != 'final' and
                       invoice.partner_id.vat is False):
                        raise ValidationError(
                            u"Para este tipo de posición fiscal el contacto"
                            " debe de tener un RNC establecido!")
                invoice.set_ncf()
        return super(AccountMove, self).post()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.one
    @api.depends('debit', 'credit')
    def _bal(self):
        self.net = self.debit-self.credit

    net = fields.Float(
        "Balance", compute=_bal, digits=dp.get_precision('Account'), store=True
        )
