# -*- coding: utf-8 -*-
from odoo import models, fields, api

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
    date_start = fields.Date(string='Fecha de asignacion')

    @api.model
    def create(self, vals): 
        vals['name'] = self.env['ir.sequence'].next_by_code('bridetobe.colas.vestidores')
        return super(bridetobeColasVestidores, self).create(vals)
