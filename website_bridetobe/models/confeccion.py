from odoo import models, fields, api


class Confeccion(models.Model):
    _name = 'bridetobe.confeccion'
    _description = 'Manejador de Confecciones BrideToBe'
    _inherit = ['mail.thread']

    name = fields.Char(string='Referencia', required=True,
                       copy=False, readonly=True,
                       index=True, default=lambda self: 'New')
    partner_id = fields.Many2one('res.partner', string="Cliente")
    tipo_confeccion = fields.Selection([('renta','Renta Exclusiva'),
                                        ('cliente','Cliente')],
                                       string="Tipo Confeccion", default="cliente")
    modista_id = fields.Many2one('hr.employee', string='Modista')
    tela = fields.Text(string="Tipo de Tela")
    materiales = fields.Text(string="Materiales")
    c_moda = fields.Selection([('dv_cliente','Dibujado por Bride to Be'),
                               ('dv_fisico','Fisico Tienda'),
                               ('dv_correo','Correo')], string="Via Suministro Moda")
    compra_tela = fields.Selection([('c_cliente','Requerida a Cliente'),
                                    ('c_tienda','Comprada Por Tienda')],
                                   string="Compra de Tela", default="c_cliente")
    event_date = fields.Date(string="Fecha del Evento")
    event_place = fields.Char(string="Lugar del Evento")

    busto = fields.Float(related="partner_id.busto",  string="Busto")
    cintura = fields.Float(related="partner_id.cintura",  string="Cintura")
    cadera = fields.Float(related="partner_id.cadera",  string="Cadera")
    falda = fields.Float(related="partner_id.falda",  string="Largo de Falda")
    espalda = fields.Float(related="partner_id.espalda",  string="Espalda")
    talle_delantero = fields.Float(related="partner_id.talle_delantero",  string="Talle Delantero")
    altura_busto = fields.Float(related="partner_id.altura_busto",  string="Altura Busto")
    separacion_busto = fields.Float(related="partner_id.separacion_busto",  string="Separacion Busto")
    talle_trasero = fields.Float(related="partner_id.talle_trasero",  string="Talle Trasero")
    largo_manga = fields.Float(related="partner_id.largo_manga",  string="Largo Manga")
    ancho_manga = fields.Float(related="partner_id.ancho_manga",  string="Ancho Manga")
    invoice_created = fields.Boolean(string="Factura Creada", default=False)
    medidas_pruebas = fields.One2many('bridetobe.medida_prueba', 'confeccion_id', string='Medidas y Pruebas')
    invoice_id = fields.Many2one('account.invoice', string="Invoice")
    costo = fields.Float(string="Costo de Confeccion")
    description = fields.Char(string="Description")

    @api.model
    def create(self, vals):
        if vals.get('modista_id') == '0' or vals.get('modista_id') == 0:
            del vals['modista_id']
        print vals
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('bridetobe.confeccion')
        result = super(Confeccion, self).create(vals)
        # self.message_post(cr, uid, ids, body=_("Form Page created"), context=None)
        return result

    @api.one
    def create_invoice(self):
        if not self.invoice_created:
            invoice_obj = self.env['account.invoice']
            self.invoice_created = True
            self.invoice_id = invoice_obj.create({'partner_id': self.partner_id.id,
                                                  'type':'out_invoice',
                                                  'name': self.name,
                                                  })
            print self.invoice_id.journal_id.default_credit_account_id.name
            self.invoice_id.invoice_line_ids.create({'name': self.description,
                                                     'quantity': 1,
                                                     'account_id': self.invoice_id.journal_id.default_credit_account_id.id,
                                                     'price_unit': self.costo,
                                                     'invoice_id': self.invoice_id.id})
            print self.invoice_id

    @api.multi
    def action_view_invoice(self):
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
        action['res_id'] = self.invoice_id.id
        return action


class MedidasPruebas(models.Model):
    _name = 'bridetobe.medida_prueba'
    _description = 'Historico Medidas/Pruebas BrideToBe'

    date_time = fields.Datetime(string='Fecha y hora de Medida/Prueba')
    modista_id = fields.Many2one('hr.employee', string="Modista")
    observaciones = fields.Text(string="Observaciones")
    confeccion_id = fields.Many2one('bridetobe.confeccion',
                                    string="Confeccion")
