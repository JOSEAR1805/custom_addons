# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    busto = fields.Float(string="Busto")
    cintura = fields.Float(string="Cintura")
    cadera = fields.Float(string="Cadera")
    falda = fields.Float(string="Largo de Falda")
    espalda = fields.Float(string="Espalda")
    talle_delantero = fields.Float(string="Talle Delantero")
    altura_busto = fields.Float(string="Altura Busto")
    separacion_busto = fields.Float(string="Separacion Busto")
    talle_trasero = fields.Float(string="Talle Trasero")
    largo_manga = fields.Float(string="Largo Manga")
    ancho_manga = fields.Float(string="Ancho Manga")