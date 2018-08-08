# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import time, date, datetime, timedelta
from odoo.exceptions import ValidationError

class bridetobeVestidores(models.Model):
    _name = 'bridetobe.vestidores'
    
    name = fields.Char(string='Codigo de Vestidor', required=True)
    status = fields.Selection([('enabled', 'Habilitado'),('disabled', 'Deshabilitado')], string='Estatus', required=True)
    description = fields.Text()
    occupation = fields.Boolean(string='Ocupación', default=False)
    time_elapsed_dressing_room = fields.Char(compute='_compute_time_elapsed_dressing_room', string='tiempo transcurrido', readonly=True)

    @api.one
    @api.depends('write_date')
    def _compute_time_elapsed_dressing_room(self):
        write_date = self.write_date.split(' ')[1]
        today = datetime.today().strftime('%H:%M:%S')
        h1 = datetime.strptime(write_date, "%H:%M:%S")
        h2 = datetime.strptime(today, "%H:%M:%S")
        resultado = str(h2 - h1)
        self.time_elapsed_dressing_room = resultado

        # aux = datetime.strptime(resultado, "%I:%M:%S")
        # if len(resultado) > 8:
        #     self.time_elapsed_dressing_room = str(aux)
        # else:
        #     self.time_elapsed_dressing_room = resultado

    @api.constrains('name')
    def _name_not_number(self):
        if str(self.name).isdigit():
            raise ValidationError('Mensaje -> '+self.name+' <-')


    _sql_constraints = [
        ('name_uniq','unique(name)','Invoice Number must be unique per Company!'),
    ]