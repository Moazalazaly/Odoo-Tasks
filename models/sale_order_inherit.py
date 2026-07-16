from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _order = 'create_date desc'

    can_confirm = fields.Boolean(
        string="Can Confirm",
        compute="_compute_can_confirm"
    )

    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve')],
        ondelete={'to_approve': 'set default'}
    )

    def _compute_can_confirm(self):
        for op in self:
            is_intern = self.env.user.is_intern
            # If they are an intern and it's waiting for approval, they can't confirm
            if is_intern:
                op.can_confirm = False
            else:
                op.can_confirm = True



    def action_confirm(self):
        user_types = (self.env.user.internship_type or '').split(', ')
        is_intern_sale = self.env.user.is_intern and 'sale' in user_types

        for sale in self:
            if sale.state =='to_approve' and is_intern_sale:
                sale.message_post(body="already sent to your admin to approve")

            else :
                if is_intern_sale:
                    sale.write({'state' : 'to_approve'})
                    sale.message_post(body="sent to your admin to approve")
                    sale.can_confirm = False
                else:
                    # 1. Filter orders that are currently in 'to_approve'
                    to_approve_orders = self.filtered(lambda sale: sale.state == 'to_approve')

                    # 2. Temporarily change their state to 'sent' WITHOUT tracking/chatter
                    if to_approve_orders:
                        to_approve_orders.with_context(tracking_disable=True).write({'state': 'sent'})

                    # 3. Call the standard Odoo confirm method on the whole recordset
                    # (Odoo will now see them as 'sent' and allow the confirmation)
                    return super(SaleOrder, self).action_confirm()

        return True