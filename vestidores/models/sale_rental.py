# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, time

class SaleRental(models.Model):
    _inherit = 'sale.rental'

    tipo_cita = fields.Char(compute='_compute_tipo_cita', string='Tipo Cita', readonly=True)
    is_queued = fields.Boolean(string='Esta en Cola', default=False)

    @api.one
    @api.depends('test_date', 'delivery_date')
    def _compute_tipo_cita(self):
        test_date = self.test_date.split(' ')[0]
        delivery_date = self.delivery_date.split(' ')[0]
        today = date.today().strftime('%Y-%m-%d')

        if test_date == delivery_date:
            self.tipo_cita = 'Probar y Entregar'
        elif test_date == today:
            self.tipo_cita = 'Probar'
        elif delivery_date == today:
            self.tipo_cita = 'Entregar'
