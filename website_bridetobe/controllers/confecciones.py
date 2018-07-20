# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from main import BridetoBe


class BridetoBeConfecciones(BridetoBe):
    confecciones_data_mandatory_fields = [
        ["event_place", "Debe digitar el Lugar del evento"],
        ["event_date", "Debe digitar la fecha del Evento"],
        ["description", "Debe digitar la descripcion del vestido"]
    ]

    def confecciones_update_partner(self, post):
        partner_obj = request.env['res.partner']
        partner = partner_obj
        seller = request.env['hr.employee'].sudo().browse(post.get("seller"))
        error = dict()
        error_message = []
        partner = partner_obj.sudo().browse(int(post.get("partner")))
        partner.write(post)

        for field_name in self.confecciones_data_mandatory_fields:
            if not post.get(field_name[0]):
                error[field_name[0]] = 'missing'
                error_message.append(field_name[1])

        if error_message:
            error['error_message'] = error_message

        render_values = {
            'error': error,
            'partner': partner,
            'confeccion_data': post,
            'country': partner.country_id,
            'product_ids': [],
            'seller': seller,
            'countries': partner.country_id.get_website_sale_countries('new'),
            'view_id': post.get('view_id'),
            'customer': True,
        }
        return render_values

    @http.route(['/confeccion'], type='http', auth="user",
                methods=['GET'], website=True, csrf=True)
    def get_confecciones(self):
        return request.redirect('/web#action='+str(request.env.ref('website_bridetobe.action_bridetobe_confeccion').id))

    @http.route(['/confecciones/partner/update'], type='http', auth="public",
                methods=['POST'], website=True, csrf=True)
    def confecciones_data(self, **post):
        render_values = self.update_partner_fields(post)
        render_values['confeccion_data'] = post
        if render_values['error']:
            return request.render('website_bridetobe.partner_data', render_values)
        else:
            render_values['modista_ids'] = request.env['hr.employee'].sudo().search(
                [('department_id', '=', request.env.ref('website_bridetobe.confecciones').id)])
            return request.render('website_bridetobe.confeccion_data', render_values)

    @http.route(['/confecciones/confeccion_data'], type='http', auth="public",
                methods=['POST'], website=True, csrf=True)
    def confecciones_validate(self, **post):
        render_values = self.confecciones_update_partner(post)
        render_values['modista_ids'] = request.env['hr.employee'].sudo().search(
            [('department_id', '=', request.env.ref('website_bridetobe.confecciones').id)])
        if render_values['error']:
            return request.render('website_bridetobe.confeccion_data', render_values)
        else:
            render_values['disabled'] = True
            confeccion = request.env['bridetobe.confeccion'].sudo().create(post)
            render_values['confirmation'] = '/confirmation'
            return request.render('website_bridetobe.confeccion_data', render_values)

    @http.route(['/confecciones/confeccion_data/confirmation'], type='http', auth="public",
                methods=['POST'], website=True, csrf=True)
    def confecciones_confirmation(self, **post):
        return request.redirect('/confecciones')