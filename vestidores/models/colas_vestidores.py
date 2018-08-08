# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import time, date, datetime, timedelta

class bridetobeColasVestidores(models.Model):
    _name = 'bridetobe.colas.vestidores'

    name = fields.Char(string='Codigo de Ticket', required=True)
    state_ticket = fields.Selection([   ('wait', 'Espera'),
                                        ('execute', 'Ejecutando'),
                                        ('closed', 'Cerrado')], 
        string='Estatus del Ticket', default='wait', required=True)
    type_queue = fields.Selection([ ('test', 'Prueba'),
                                    ('making', 'Confección')], 
        string='Tipo de Cola', default='making', required=True)
    encolado = fields.Boolean(string='Encolado', default=True)
    sale_rental_id = fields.Many2one("sale.rental", string="Alquiler de Venta")
    cliente_id = fields.Many2one("res.partner", string="Cliente")
    modista_id = fields.Many2one(related="sale_rental_id.modista", string="Modista")
    producto_ids = fields.Many2many("product.template", string="Productos")
    date_start = fields.Datetime(string='Fecha de asignacion')
    time_elapsed = fields.Char(compute='_compute_time_elapsed', string='tiempo transcurrido', readonly=True)

    @api.one
    @api.depends('date_start')
    def _compute_time_elapsed(self):
        date_start = self.date_start.split(' ')[1]
        today = datetime.today().strftime('%H:%M:%S')
        h1 = datetime.strptime(date_start, "%H:%M:%S")
        h2 = datetime.strptime(today, "%H:%M:%S")
        resultado = str(h2 - h1)
        if len(resultado) > 8:
            self.time_elapsed_dressing_room = "23:59:59"
        else:
            self.time_elapsed_dressing_room = str(h2 - h1)

    @api.model
    def create(self, vals): 
        vals['name'] = self.env['ir.sequence'].next_by_code('bridetobe.colas.vestidores')
        return super(bridetobeColasVestidores, self).create(vals)
