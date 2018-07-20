# -*- coding: utf-8 -*-

from odoo import models, fields, api

class bridetobeAuditoriaColas(models.Model):
    _name = 'bridetobe.auditoria.colas'

    empleado_ids = fields.One2many()
    tickets_ids = fields.One2One()
    cliente_ids = fields.One2many()
    modista_ids = fields.One2many()
    vestidor_ids = fields.One2many()
    time_start = fields.date()
    time_end = fields.date()


