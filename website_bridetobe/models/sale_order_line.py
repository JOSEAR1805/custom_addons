from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_order_line_procurement(
            group_id=group_id)
        if (self.product_id.rented_product_id and self.rental_type == 'new_rental'):
            product = self.env['product.product'].search(
                [('product_tmpl_id', '=', self.product_id.rented_product_id.id)], limit=1)
            res.update({
                'product_id': product.id,
            })
        return res

    start_date = fields.Date(string='Start Date', readonly=False)
    end_date = fields.Date(string='End Date', readonly=False)
