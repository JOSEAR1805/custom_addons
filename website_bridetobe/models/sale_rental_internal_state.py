from odoo import models, fields


class SaleRentalInternalState(models.Model):
    _name = "sale.rental.internal.state"
    _description = "States for Rentals"
    _order = "sequence"

    name = fields.Char(string="Description", required=True)
    sequence = fields.Integer(string="Sequence",
                              default=lambda self: max([a.sequence for a in self.search([(1, '=', 1)])] or [0]) + 1)
    group = fields.Many2one('res.groups', string="Gupo que visualiza", default=False)
    message_send = fields.Boolean(string='Send Messages')
    state_color = fields.Selection([("skyblue", "BLUE"),
                                    ("gray", "GRAY"),
                                    ("purple", "PURPLE"),
                                    ("lightgreen", "GREEN"),
                                    ("brown", "BROWN"), ], string="Color")
    message_body = fields.Html(string="Message Body",
                               help="""
                               Valores que pueden ser utilizados para crear el mensaje
                               =======================================================
                               {0} : Cliente
                               {1} : Articulo
                               {2} : Estado
                               {3} : Modista
                               {4} : Orden Relacionada
                               {5} : Fecha de Prueba
                               {6} : Fecha Entrega
                               =======================================================
                               Ejemplo de uso: 
                                * Hola {0} el articulo {1} de su orden {4} a cambiado su
                                  estado a {2} y esta siendo trabajado por la modista {3}  
                               """)
    sale_order_state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Sale Order Status',
        help="Si esta seleccionado solo las ordenes utilizan este Estado y sus configuraciones")

    _sql_constraints = [
        ('sale_internal_state_uniq', 'unique(name)', 'Este estado ya existe'),
        ('sale_internal_order_state_uniq', 'unique(sale_order_state)', 'Relacion Duplicada')
    ]
