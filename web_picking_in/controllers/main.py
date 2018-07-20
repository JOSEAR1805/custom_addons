from odoo import http
from odoo.http import request
from ...web_picking.controllers.main import WebCustomerDelivery

class DeliveryIn(WebCustomerDelivery):
    page_header = 'Warehouse Receipts'
    page_header_details = 'Warehouse Delivery Details'

    @http.route(['/picking_in'], type='http', auth="user", methods=['GET'], website=True)
    def call_get_warehouse_in(self, **get):
        render_values = super(DeliveryIn, self).get_warehouse('incoming',
                                                              'assigned')
        render_values['page_header'] = self.page_header
        render_values['form_action'] = '/picking_in_details'
        render_values['form_method'] = 'post'
        return request.render('web_picking.web_picking_list',
                              render_values)

    @http.route(['/picking_in_details'], type='http', auth="user", methods=['POST'], website=True)
    def call_show_delivery_details_in(self, **post):
        render_values = super(DeliveryIn, self).show_delivery_details(post,
                                                                      'incoming',
                                                                      'assigned')
        render_values['form_method'] = 'post'
        if post.get('submit') != 'search' and post.get('picking_id'):
            render_values['page_header'] = self.page_header
            render_values['form_action'] = '/picking_in_complete'
            return request.render('web_picking.web_picking_details',
                                  render_values)
        elif post.get('submit') == 'search':
            render_values['page_header'] = self.page_header_details
            render_values['form_action'] = '/picking_in_details'
            return request.render('web_picking.web_picking_list',
                                  render_values)

    @http.route(['/picking_in_complete'], type='http', auth="user", methods=['POST'], website=True)
    def call_complete_delivery_in(self, **post):
        super(DeliveryIn, self).complete_delivery(post)
        return request.render('web_picking.web_picking_signature', {'form_action': '/picking_in'})