# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class bridetobeVestidores(models.Model):
    _name = 'bridetobe.vestidores'
    
    name = fields.Char(string='Codigo de Vestidor', required=True)
    status = fields.Selection([('enabled', 'Habilitado'),('disabled', 'Deshabilitado')], string='Estatus', required=True)
    description = fields.Text()
    occupation = fields.Boolean(string='Ocupación', default=False)

    @api.constrains('name')
    def _name_not_number(self):
        if str(self.name).isdigit():
            raise ValidationError('Mensaje -> '+self.name+' <-')


    _sql_constraints = [
        ('name_uniq','unique(name)','Invoice Number must be unique per Company!'),
    ]