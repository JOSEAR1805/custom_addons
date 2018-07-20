from odoo import http
from odoo.http import request


class WebCustomerDelivery(http.Controller):
    def get_warehouse(self, picking_type, state):
        picking_ids = request.env['stock.picking'].search([('state', '=', state),
                                                           ('picking_type_code', '=', picking_type)])
        render_values = {
            'error': dict(),
            'picking_ids': picking_ids
        }
        return render_values

    def show_delivery_details(self, post, picking_type, state):
        error = dict()
        error_message = []
        if post.get('submit') != 'search' and post.get('picking_id'):
            picking_ids = request.env['stock.picking'].browse(int(post.get('picking_id')))
            if picking_ids.name:
                return {
                    'error': dict(),
                    'picking_id': picking_ids,
                }
        elif post.get('submit') == 'search':
            picking_ids = False
            if post.get('search'):
                picking_ids = request.env['stock.picking'].search(['|', ('name', 'ilike', post.get('search')),
                                                                   ('origin', 'ilike', post.get('search')),
                                                                   ('picking_type_code', '=', picking_type),
                                                                   ('state', '=', state)])
                if not picking_ids:
                    error_message.append('Delivery does not exist')
                    error['error_message'] = error_message
            if not picking_ids:
                picking_ids = request.env['stock.picking'].search([('state', '=', state),
                                                                   ('picking_type_code', '=', picking_type)])
            return {
                'error': error,
                'picking_ids': picking_ids,
            }

    def complete_delivery(self, post):
        picking_id = request.env['stock.picking'].browse(int(post.get('picking_id')))
        for pack_operation_product_id in picking_id.pack_operation_product_ids:
            pack_operation_product_id.qty_done = pack_operation_product_id.product_qty
        return picking_id.do_new_transfer()