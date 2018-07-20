# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import json

from odoo.addons.web.controllers.main import Home


class Website(Home):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        page = 'website_bridetobe.homepage'
        return self.page(page)


class BridetoBe(http.Controller):
    update_partner_mandatory_fields = [
        ["country_id", "Debe seleccionar un Pais"],
        ["name", "Digite su nombre"],
        ["mobile", "Digite su numero de movil"],
        ["phone", "Digite su numero de Telefono"],
        ["email", "Digite su Email"],
        ["street", "Digite la Calle"],
        ["city", "Debe digitar su ciudad"]]
    # ["vat", "Digite RNC / Cedula"],

    event_data_mandatory_fields = [
        ["cadera", "Debe digitar la medida de la Cadera"],
        ["event_place", "Debe digitar el Lugar del evento"],
        ["busto", "Debe digitar la medida del Busto"],
        ["event_date", "Debe digitar la fecha del Evento"],
        ["cintura", "debe digitar la medida de la Cintura"]]

    @http.route(['/shop'], type='http', auth="public", methods=['GET'], website=True)
    def homepage(self, **get):
        view_id = request.httprequest.full_path.replace('/', '').replace('?', '')
        return request.render('website_bridetobe.homepage', {'error': dict(), 'view_id': view_id})

    @http.route(['/renta'], type='http', auth="public", methods=['GET'], website=True)
    def renta(self, **get):
        view_id = request.httprequest.full_path.replace('/', '').replace('?', '')
        return request.render('website_bridetobe.set_seller', {'error': dict(), 'view_id': view_id})

    @http.route(['/renta'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def get_seller(self, **post):
        render_values = self.validate_seller(post.get('seller_code'), post)
        if render_values['error']:
            return request.render('website_bridetobe.set_seller', render_values)
        else:
            return request.render('website_bridetobe.set_partner', render_values)

    @http.route(['/renta/partner'], type='http', auth="public", methods=['POST'],
                website=True, csrf=True)
    def get_partner(self, **post):
        error = dict()
        error_message = []
        partner_ids = []
        form_action = ''
        multi_partner = False
        if post.get('partner_vat', False):
            partner_ids = request.env['res.partner'].sudo().search(['|', ('name', 'ilike', post.get('partner_vat')),
                                                                    ('vat', '=', post.get('partner_vat'))])
            qweb_template = 'web_quote.web_quote_partner_list'
            form_action = '/%s/partner?view_id=%s&seller=%s' % (
                post.get('view_id'), post.get('view_id'), post.get('seller'))

        elif post.get('partner_id', False):
            partner_ids = request.env['res.partner'].sudo().browse(int(post.get('partner_id')))
            qweb_template = 'website_bridetobe.partner_data'
            form_action = 'website_bridetobe.partner_data'
        # if len(partner_ids) > 1:
        #     qweb_template = 'web_quote.web_quote_partner_list'
        #     form_action = '/%s/partner?view_id=%s&seller=%s' % (
        #     post.get('view_id'), post.get('view_id'), post.get('seller'))
        # else:
        #     error['partner_vat'] = 'missing'
        #     error_message.append('Cliente no Existe')
        #     error['error_message'] = error_message
        #     form_action = '/web_quote/search_partner'
        #     qweb_template = 'website_bridetobe.partner_data'
        if not partner_ids:
            error['partner_vat'] = 'missing'
            error_message.append('Cliente no Existe')
            error['error_message'] = error_message
            form_action = '/web_quote/search_partner'
            qweb_template = 'website_bridetobe.partner_data'
        return request.render(qweb_template,
                              {'error': error,
                               'partner_temp': post,
                               'country_ids': request.env['res.country'].sudo().search([]),
                               'form_action': form_action,
                               'form_method': 'post',
                               'view_id': post.get('view_id'),
                               'seller': request.env['hr.employee'].sudo().browse(int(post.get("seller"))),
                               'partner_ids': partner_ids,
                               'countries': request.env['res.country'].sudo().search([]),
                               'partner': partner_ids})
        # render_values = self.validate_partner(post.get('partner_vat'), post)
        # render_values['seller'] = request.env['hr.employee'].sudo().browse(int(post.get("seller")))
        #
        # if post.get('submit') == 'new':
        #     render_values['partner_temp'] = {'vat': post.get('partner_vat'),
        #                                      'customer_code': post.get('partner_vat')}
        #     render_values['country_id'] = request.env.user.company_id.country_id.id
        #     return request.render('website_bridetobe.partner_data', render_values)
        # else:
        #     if render_values['error']:
        #         return request.render('website_bridetobe.set_partner', render_values)
        #     else:
        #         return request.render('website_bridetobe.partner_data', render_values)

    @http.route(['/renta/partner/update'], type='http', auth="public",
                methods=['POST'], website=True, csrf=True)
    def update_partner(self, **post):
        render_values = self.update_partner_fields(post)
        if render_values['error']:
            return request.render('website_bridetobe.partner_data', render_values)
        else:
            return request.render('website_bridetobe.event_data', render_values)

    def validate_seller(self, seller_code, post):
        seller = request.env['hr.employee'].sudo().search([('seller_code', '=', seller_code)])
        error = dict()
        error_message = []
        if 'submitted' in post:
            if not post.get('seller_code'):
                error['seller_code'] = 'missing'
                error_message.append(_('Debe digitar el Codigo de vendedor'))
            if post.get('seller_code') and not seller:
                error['seller_code'] = 'error'
                error_message.append(_('Codigo de Vendedor invalido'))
        if error_message:
            error['error_message'] = error_message
        render_values = {
            'error': error,
            'seller': seller,
            'view_id': post.get('view_id'),
        }

        return render_values

    def validate_partner(self, partner_vat, post):
        partner = request.env['res.partner'].sudo().search(
            ['|', ('vat', '=', partner_vat), ('customer_code', '=', partner_vat)])
        error = dict()
        error_message = []

        if 'submitted' in post:
            if not post.get('partner_vat'):
                error['partner_vat'] = 'missing'
                error_message.append(_('Debe digitar el Codigo de Cliente'))
            if post.get('partner_vat') and not partner:
                error['partner_vat'] = 'error'
                error_message.append(_('Cliente no Existe'))
        if error_message:
            error['error_message'] = error_message

        render_values = {
            'error': error,
            'partner': partner,
            'partner_vat': post.get('partner_vat'),
            'country': partner.country_id,
            'customer_code': post.get('partner_vat'),
            'countries': partner.country_id.get_website_sale_countries('new'),
            'view_id': post.get('view_id'),
        }
        return render_values

    def update_partner_fields(self, post):
        partner_obj = request.env['res.partner']
        partner = partner_obj
        seller = request.env['hr.employee'].sudo().browse(post.get("seller"))
        error = dict()
        error_message = []

        if 'submitted' in post:
            for field_name in self.update_partner_mandatory_fields:
                if not post.get(field_name[0]):
                    error[field_name[0]] = 'missing'
                    error_message.append(field_name[1])
            if not error:
                if post.get("partner"):
                    partner = partner_obj.sudo().browse(int(post.get("partner")))
                    if post.get('name') == partner.name:
                        del (post['name'])
                    partner.write(post)
                else:
                    try:
                        partner = partner.sudo().create(post)
                    except (Exception), err:
                        error['vat'] = 'duplicate'
                        error_message.append(err[0])
        if error_message:
            error['error_message'] = error_message
        render_values = {
            'error': error,
            'partner': partner,
            'partner_temp': post,
            'country': partner.country_id,
            'product_ids': [],
            'seller': seller,
            'countries': partner.country_id.get_website_sale_countries('new'),
            'view_id': post.get('view_id'),
            'customer': True,
        }
        return render_values

    @http.route(['/renta/event_data'], type='http', auth="public", methods=['POST'],
                website=True, csrf=True)
    def event_data(self, **post):
        partner = request.env['res.partner'].sudo().browse(int(post.get("partner")))
        seller = request.env['hr.employee'].sudo().browse(post.get("seller"))
        partner.write({'busto': post.get('busto'),
                       'cintura': post.get('cintura'),
                       'cadera': post.get('cadera'),
                       'falda': post.get('falda')})
        error = dict()
        product_ids = []
        product_valid = []
        if post.get('item_code') and post.get('product_barcode'):
            product_barcode = post.get('product_barcode') + ',' + str(post.get('item_code'))
        elif not post.get('item_code') and post.get('product_barcode'):
            product_barcode = str(post.get('product_barcode'))
        else:
            product_barcode = str(post.get('item_code'))
        if post.get('event_date') and post.get('event_place'):
            for code in product_barcode.split(','):
                product = request.env['product.template'].sudo().search([('barcode', '=', code),
                                                                         ('rented_product_id', '!=', False)])
                if product:
                    date = datetime.strptime(post.get('event_date'), DEFAULT_SERVER_DATE_FORMAT)
                    date_start = date - timedelta(days=date.weekday())
                    date_end = date_start + timedelta(days=7)

                    product_availability = request.env['sale.rental'].sudo().search(
                        [('rental_product_id', '=', product.id),
                         ('start_date', '<=', datetime.strftime(date_end, DEFAULT_SERVER_DATE_FORMAT)),
                         ('start_date', '>=', datetime.strftime(date_start, DEFAULT_SERVER_DATE_FORMAT)),
                         ('state', '!=', 'cancel')])
                    if product_availability:
                        product_barcode = product_barcode.replace(product.barcode, '')
                        error['error_message'] = [
                            u''.join(("Articulo ", product.name, " no esta disponible")).encode('utf-8')]
                    elif product.barcode not in product_valid:
                        product_valid.append(product.barcode)
                        product_id = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product.id),
                                                                                   ('barcode', '=', product.barcode)])
                        product_ids.insert(0, {"barcode": product.barcode,
                                               "name": product.name,
                                               "image": product.image,
                                               "price": product.list_price,
                                               "id": product_id.id})
                    else:
                        product_barcode = product_barcode.replace(product.barcode + ',', '', 1)
                        error['error_message'] = [
                            u''.join(("El articulo ", product.name, " ya fue agregado a la orden")).encode('utf-8')]
                else:
                    if code == post.get('item_code'):
                        error['error_message'] = ["Codigo de Articulo Invalido"]
            if post.get('submit') == 'get_item':
                render_values = {
                    'error': error,
                    'partner': partner,
                    'country': partner.country_id,
                    'seller': seller,
                    'countries': partner.country_id.get_website_sale_countries('new'),
                    'view_id': post.get('view_id'),
                    'product_ids': product_ids,
                    'product_barcode': product_barcode,
                    'event_date': post.get('event_date'),
                    'event_place': post.get('event_place'),
                    'comments': post.get('comments')
                }
                return request.render('website_bridetobe.event_data', render_values)
            elif post.get('submit') == 'validate':
                render_values = self.validate_event_data(post, product_ids, product_barcode)
                if render_values['error']:
                    return request.render('website_bridetobe.event_data', render_values)
                else:
                    data = {
                        "partner_id": int(post.get('partner')),
                        "event_date": post.get('event_date'),
                        "event_place": post.get('event_place'),
                        "busto": post.get('busto'),
                        "cintura": post.get('cintura'),
                        "cadera": post.get('cadera'),
                        "default_start_date": datetime.strptime(post.get('event_date'),
                                                                DEFAULT_SERVER_DATE_FORMAT) - relativedelta(days=7),
                        "default_end_date": post.get('event_date'),
                        "comments": post.get('comments'),
                        "seller_id": int(post.get('seller'))
                    }
                    order_id = request.env['sale.order'].sudo().create(data)
                    render_values['order'] = order_id
                    for product_id in product_ids:
                        request.env['sale.order.line'].sudo().create({
                            'order_id': order_id.id,
                            'rental_type': 'new_rental',
                            'number_of_days': 1,
                            'rental_qty': 1,
                            'customer_lead': 1,
                            'start_date': post.get('event_date'),
                            'end_date': post.get('event_date'),
                            'product_id': product_id.get('id'),
                            'name': product_id.get('name'),
                            'product_uom_qty': 1,
                            'price_unit': product_id.get('price')
                        })

                return request.render('website_bridetobe.order_confirmation', render_values)
        else:
            render_values = self.validate_event_data(post, product_ids, None)
            return request.render('website_bridetobe.event_data', render_values)

    def validate_event_data(self, post, product_ids, product_barcode):
        partner = request.env['res.partner'].sudo().browse(int(post.get("partner") or post.get('partner_id')))
        seller = request.env['hr.employee'].sudo().browse(post.get("seller"))
        error = dict()
        error_message = []

        for field_name in self.event_data_mandatory_fields:
            if not post.get(field_name[0]):
                error[field_name[0]] = 'missing'
                error_message.append(field_name[1])
        if product_barcode is not None:
            if not request.env['product.template'].sudo().search(
                    [('barcode', 'in', post.get('product_barcode').split(","))]):
                error['product_barcode'] = 'missing'
                error_message.append('No ha Seleccionado Productos')
        if error_message:
            error['error_message'] = error_message
        render_values = {
            'error': error,
            'partner': partner,
            'country': partner.country_id,
            'seller': seller,
            'countries': partner.country_id.get_website_sale_countries('new'),
            'view_id': post.get('view_id'),
            'product_ids': product_ids,
            'product_barcode': product_barcode,
            'event_date': post.get('event_date'),
            'event_place': post.get('event_place'),
        }
        return render_values

    @http.route(['/renta/order_confirmation'], type='http', auth="public",
                methods=['POST'], website=True, csrf=True)
    def order_confirmation(self, **post):
        order_id = request.env['sale.order'].sudo().browse(int(post.get('order')))
        if order_id.action_confirm():
            order_id.action_invoice_create()
            # order_id.action_done()
            return request.render('website_bridetobe.homepage', {'order': order_id})

    @http.route(['/search_available'], type='http', auth="public", methods=['GET'],
                website=True, csrf=True)
    def search_available(self, **post):
        return request.render('website_bridetobe.search_available', {})

    @http.route(['/search_available_calendar'], type='http', auth="public", methods=['POST'],
                website=True, csrf=True)
    def search_available_calendar(self, **post):
        error = dict()
        error_message = []
        product_barcode = post.get('product_barcode')
        product_id = request.env['product.template'].sudo().search(['|', ('barcode', '=', product_barcode),
                                                                    ('name', 'ilike', product_barcode),
                                                                    ('rented_product_id', '!=', False)])
        if not product_barcode:
            error['product_barcode'] = 'missing'
            error_message.append('Digite Codigo de Producto')
        elif not product_id:
            error['product_barcode'] = 'missing'
            error_message.append('Codigo de Producto Invalido')
        if error_message:
            error['error_message'] = error_message
            render_values = {
                'error': error
            }
            return request.render('website_bridetobe.search_available', render_values)

        render_values = {
            'product_id': product_id
        }
        return request.render('website_bridetobe.search_available_calendar', render_values)

    @http.route(['/get_events'], type='http', auth="public", methods=['POST'],
                website=True, csrf=True)
    def get_events(self, **post):
        start_date = post.get('start')
        end_date = post.get('end')
        product_id = post.get('product_id')
        sale_rental_ids = []
        product_ids = []
        for product_rental in product_id.replace('[', '').replace(']', '').split(','):
            product_ids.append(int(product_rental))
        sale_rental_search_ids = request.env['sale.rental'].sudo().search(
            [('start_date', '>=', start_date), ('start_date', '<=', end_date),
             ('rental_product_id', 'in', product_ids)])
        for sale_rental_id in sale_rental_search_ids:
            sale_rental_ids.append({'title': sale_rental_id.rental_product_id.barcode,
                                    'start': sale_rental_id.start_date})
        return json.dumps(sale_rental_ids)
