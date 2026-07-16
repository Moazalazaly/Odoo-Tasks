from odoo import api, fields, models, tools

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        user_types = (self.env.user.internship_type or '').split(', ')
        is_intern_purchase = self.env.user.is_intern and 'purchase' in user_types

        for order in self:
            if order.state =='to approve':
                order.message_post(body="already sent to your admin to approve")

            else :
                if is_intern_purchase:
                    order.state = "to approve"
                    order.message_post(body="sent to your admin to approve")
                else:
                    super(PurchaseOrder, order).button_confirm()

        return True

    @api.model
    def retrieve_dashboard(self):

        result = super().retrieve_dashboard()
        result['all_purchase_orders'] = self.env['purchase.order'].search_count([
            ('state', '=', 'purchase'),
        ])
        return result


