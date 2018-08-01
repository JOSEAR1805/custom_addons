# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from datetime import date

class webVestidores(http.Controller):

    @http.route(['/dressing_room'], type='http', auth='public', website=True)
    def dressing_room_test(self):
        return request.render('vestidores.vestidores')

    @http.route(['/dressing_room_assignation'], type='http', auth="public", website=True)
    def get_dressing_room_assignation(self, **post):
        item_cola = request.env['items.colas'].create({
            'vestidores_ids': post.get('vestidor_id'),
            'colas_vestidores_ids': post.get('cola_vestidor_id'),
        })
        update_occupation = request.env['bridetobe.vestidores'].browse(
            int(post.get('vestidor_id'))).write({'occupation': True})
        update_encolado = request.env['bridetobe.colas.vestidores'].browse(
            int(post.get('cola_vestidor_id'))).write({'encolado': False})
        return request.redirect(post.get('redirect_to'))

    def set_queue(self):
        colas_vestidores = request.env['bridetobe.colas.vestidores'].search([
            '&',
            '&',
            ('date_start','>=',str(date.today())+" 00:00:00"),
            ('date_start','<=',str(date.today())+" 23:59:59"),
            ('encolado','=','True')
        ])
        colas_vestidores_conf = []
        colas_vestidores_test = []
        for aux in colas_vestidores:
            if aux.type_queue == 'making':
                colas_vestidores_conf.append(aux)
            elif aux.type_queue == 'test':
                colas_vestidores_test.append(aux)
        vestidores = request.env['bridetobe.vestidores'].search([
            ('status','=','enabled')
        ])
        items_colas = request.env['items.colas'].search([])
        render_values = {
            'colas_vestidores_conf': colas_vestidores_conf,
            'colas_vestidores_test': colas_vestidores_test,
            'vestidores': vestidores,
            'items_colas': items_colas
        }
        return render_values

    @http.route(['/queue_making'], type='http', auth="public", website=True)
    def get_queue_making(self):
        values = self.set_queue()
        return request.render('vestidores.page_queue_making', values)

    @http.route(['/queue_test'], type='http', auth="public", website=True)
    def get_queue_test(self):
        values = self.set_queue()
        return request.render('vestidores.page_queue_test', values)

    def validate_customer(self, customer, post):
        res_partner = None
        error = dict()
        error_message = []
        sale_rentals = []
        if 'submitted' in post:
            if post.get('customer'):
                res_partner = request.env['res.partner'].sudo().search([
                    '|',
                    ('vat', '=', customer),
                    ('customer_code','=', customer)
                ])
                sale_rentals = request.env['sale.rental'].search([
                    '&',
                    '&',
                    '|',
                    '&',
                    ('delivery_date','>=',str(date.today())+" 00:00:00"),
                    ('delivery_date','<=',str(date.today())+" 23:59:59"),
                    '&',
                    ('test_date','>=',str(date.today())+" 00:00:00"),
                    ('test_date','<=',str(date.today())+" 23:59:59"),
                    ('partner_id','=', res_partner.id),
                    ('is_queued','=',False)
                ])
                if not res_partner:
                    error['customer'] = 'error'
                    error_message.append(_('Número de Identificación no esta registrado'))
                elif res_partner and not sale_rentals:
                    error['customer'] = 'error'
                    error_message.append(_('Número de Identificación no posee cita para hoy'))
            else:
                    error['customer'] = 'missing'
                    error_message.append(_('Debe Ingresar su Número de Identificación'))
        if error_message:
            error['error_message'] = error_message
        render_values = {
            'error': error,
            'sale_rentals': sale_rentals,
            'res_partner': res_partner,
            'view_id': post.get('view_id'),
        }
        return render_values

    @http.route(['/quotes'], type='http', auth="public", methods=['GET'], website=True)
    def quotes(self, **get):
        view_id = request.httprequest.full_path.replace('/', '').replace('?', '')
        return request.render('vestidores.page_quotes_form', {'error': dict(), 'view_id': view_id})

    @http.route(['/quotes'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def get_customer(self, **post):
        render_values = self.validate_customer(post.get('customer'), post)
        if render_values['error']:
            return request.render('vestidores.page_quotes_form', render_values)
        else:
            return request.render('vestidores.page_quotes', render_values)

    @http.route(['/take_turn_in_queue'], type='http', auth="public", website=True)
    def take_turn_in_queue(self, **post):
        colas_vestidores = request.env['bridetobe.colas.vestidores'].create({
            'sale_rental_id': post.get('sale_rental_id'),
            'cliente_id': post.get('cliente_id'),
            'producto_ids': [(4, [int(post.get('producto_ids'))])],
            'date_start': date.today(),
        })
        sale_rental = request.env['sale.rental'].browse(int(post.get('sale_rental_id'))).write(
            {'is_queued': True}
        )
        return request.redirect(post.get('redirect_to'))
        
    @http.route(['/modista'], type='http', auth="public", website=True)
    def get_modista(self):
        items_colas = request.env['items.colas'].search([])
        return request.render('vestidores.page_modistas', {'items_colas': items_colas})

    @http.route(['/views_tv'], type='http', auth="public", website=True )
    def index_dressing_room(self, **kw):
        items_colas = request.env['items.colas'].search([])
        return request.render('vestidores.page_queue_tv', {
            'items_colas': items_colas
        })

    def validate_partner(self, partner_vat, post):
        error = dict()
        error_message = []
        product_ids = []
        partner_ids = []
        if 'submitted' in post:
            if post.get('partner_vat'):
                partner_ids = request.env['res.partner'].sudo().search([
                    '|',
                    '|',
                    ('vat', '=', partner_vat), 
                    ('customer_code', '=', partner_vat),
                    ('name', 'ilike', partner_vat)
                ])
                product_ids = request.env['product.template'].sudo().search([('rental_code','!=','')])
                if not partner_ids:
                    error['partner_vat'] = 'error'
                    error_message.append(_('Cliente no Existe'))
            else:
                    error['partner_vat'] = 'missing'
                    error_message.append(_('Debe ingresar identificación del Cliente'))

        if error_message:
            error['error_message'] = error_message
        render_values = {
            'error': error,
            'partner_ids': partner_ids,
            'product_ids': product_ids,
            'partner_vat': post.get('partner_vat'),
            'customer_code': post.get('partner_vat'),
            'view_id': post.get('view_id'),
        }
        return render_values

    @http.route(['/assignment_to_test'], type='http', auth="public", methods=['GET'], website=True)
    def assignment_to_test(self, **get):
        view_id = request.httprequest.full_path.replace('/', '').replace('?', '')
        return request.render('vestidores.page_queue_test_set_partner_form', {'error': dict(), 'view_id': view_id})

    @http.route(['/assignment_to_test'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def get_partner(self, **post):
        render_values = self.validate_partner(post.get('partner_vat'), post)
        if render_values['error']:
            return request.render('vestidores.page_queue_test_set_partner_form', render_values)
        else:
            return request.render('vestidores.page_queue_test_set_partner', render_values)

    @http.route(['/test_queue_assignation'], type='http', auth="public", website=True)
    def get_test_queue_assignation(self, **post):
        colas_vestidores = request.env['bridetobe.colas.vestidores'].create({
            'cliente_id': post.get('cliente_id'),
            'producto_ids': [(6, 0, [int(x) for x in request.httprequest.form.getlist('products[]')])],
            'type_queue': 'test',
            'date_start': date.today(),
        })
        return request.redirect(post.get('redirect_to'))
        
    @http.route(['/register_customer'], type='http', auth='public', website=True, methods=['GET'])
    def render_register_customer(self, **get):
        error = dict()
        error_message = []
        partner_ids = []
        qweb_template = 'vestidores.id_partner_data'
        product_ids = request.env['product.template'].sudo().search([('rental_code','!=','')])

        return request.render(qweb_template,{
            'error': error,
            'partner_temp': get,
            'country_ids': request.env['res.country'].sudo().search([]),
            'form_method': 'post',
            'seller': request.env['hr.employee'],
            'view_id': get.get('view_id'),
            'partner_ids': request.env['res.partner'],
            'countries': request.env['res.country'].sudo().search([]),
            'partner': request.env['res.partner'],
            'product_ids': product_ids
        })

    @http.route(['/save_customer'], type='http', auth="public", website=True)
    def get_customer_new(self, **post):
        customers = request.env['res.partner'].create({
            'name': post.get('name'),
            'customer_code': post.get('customer_code'),
            'mobile': post.get('mobile'),
            'phone': post.get('phone'),
            'vat': post.get('vat'),
            'email': post.get('email'),
            'street': post.get('street'),
            'city': post.get('city'),
            'country_id' : int(post.get('country_id'))
        })
        res_partners = request.env['res.partner'].search([
            '&',
            ('create_date','>=',str(date.today())+" 00:00:00"),
            ('create_date','<=',str(date.today())+" 23:59:59")
        ])
        for res_partner in res_partners:
            if res_partner.vat == post.get('vat') and res_partner.customer_code == post.get('customer_code'):
                colas_vestidores = request.env['bridetobe.colas.vestidores'].create({
                    'cliente_id': res_partner.id,
                    'producto_ids': [(6, 0, [int(x) for x in request.httprequest.form.getlist('products[]')])],
                    'type_queue': 'test',
                    'date_start': date.today(),
                })
        return request.redirect('/queue_test')

    @http.route(['/end_process_dressing_room'], type='http', auth="public", website=True)
    def get_end_process_dressing_room(self, **post):
        update_occupation_vestidor = request.env['bridetobe.vestidores'].browse(
            int(post.get('vestidor_id'))).write({'occupation': False})
        update_ticket_cola_vestidor = request.env['bridetobe.colas.vestidores'].browse(
            int(post.get('cola_vetidor_id'))).write({'state_ticket': 'closed'})
        delete_item = request.env['items.colas'].browse(int(post.get('item_id'))).unlink()
        return request.redirect(post.get('redirect_to'))

# ----------------------PRUEBAS DE JOSE ARTIGAS---------------------------

    @http.route(['/quotes_test'], type='http', auth="public", website=True)
    def quotes_test(self):
        sale_rentals = request.env['sale.rental'].search([
            '&',
            '|',
            '&',
            ('delivery_date','>=',str(date.today())+" 00:00:00"),
            ('delivery_date','<=',str(date.today())+" 23:59:59"),
            '&',
            ('test_date','>=',str(date.today())+" 00:00:00"),
            ('test_date','<=',str(date.today())+" 23:59:59"),
            ('is_queued','=',False)
        ])
        return request.render('vestidores.page_quotes_test', {'sale_rentals': sale_rentals})

    @http.route(['/dressing_room_test'], type='http', auth="public", website=True)
    def get_dressing_room(self):
        colas_vestidores_conf = request.env['bridetobe.colas.vestidores'].search([
            '&',
            '&',
            '&',
            ('date_start','>=',str(date.today())+" 00:00:00"),
            ('date_start','<=',str(date.today())+" 23:59:59"),
            ('type_queue','=','making'),
            ('encolado','=','True')
        ])
        colas_vestidores_test = request.env['bridetobe.colas.vestidores'].search([
            '&',
            '&',
            '&',
            ('date_start','>=',str(date.today())+" 00:00:00"),
            ('date_start','<=',str(date.today())+" 23:59:59"),
            ('type_queue','=','test'),
            ('encolado','=','True')
        ])
        vestidores = request.env['bridetobe.vestidores'].search([
            ('status','=','enabled')
        ])
        items_colas = request.env['items.colas'].search([])
        return request.render('vestidores.page_dressing_room',{
            'colas_vestidores_conf': colas_vestidores_conf,
            'colas_vestidores_test': colas_vestidores_test,
            'vestidores': vestidores,
            'items_colas': items_colas
        })