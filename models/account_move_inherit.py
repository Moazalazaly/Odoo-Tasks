from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

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



    def action_post(self):
        user_types = (self.env.user.internship_type or '').split(', ')
        is_intern_invoicing = self.env.user.is_intern and 'account' in user_types
        print(self.env.user.is_intern)
        print('account' in user_types)

        for invoice in self:
            if invoice.state =='to_approve' and is_intern_invoicing:
                invoice.message_post(body="already sent to your admin to approve")

            else :
                if is_intern_invoicing:
                    invoice.write({'state' : 'to_approve'})
                    invoice.message_post(body="sent to your admin to approve")
                else:
                    # 1. Filter orders that are currently in 'to_approve'
                    to_approve_orders = self.filtered(lambda invoice: invoice.state == 'to_approve')

                    # 2. Temporarily change their state to 'draft' WITHOUT tracking/chatter
                    if to_approve_orders:
                        to_approve_orders.with_context(tracking_disable=True).write({'state': 'draft'})

                    # 3. Call the standard Odoo confirm method on the whole recordset
                    # (Odoo will now see them as 'draft' and allow the confirmation)
                    return super(AccountMove, self).action_post()

        return True