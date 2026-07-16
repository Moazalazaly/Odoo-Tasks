from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    _order = "create_date desc"

    # Replace your current can_confirm field with this:
    can_confirm = fields.Boolean(
        string="Can Confirm",
        compute="_compute_can_confirm"
    )



    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve')],
        ondelete={'to_approve': 'set draft'}
    )

    def _compute_can_confirm(self):
        for object in self:
            is_intern = self.env.user.is_intern
            if is_intern:
                object.can_confirm = False
            else:
                object.can_confirm = True

    def action_confirm(self):
        user_types = (self.env.user.internship_type or '').split(', ')
        print(user_types)
        is_intern_stock = self.env.user.is_intern and 'stock' in user_types
        print(self.env.user.is_intern)
        print(self.env.user.internship_type)


        for inventory_operation in self:

            if inventory_operation.state == 'to_approve' and is_intern_stock:
                inventory_operation.message_post(body="already sent to your admin to approve")

            else:
                if is_intern_stock:
                    inventory_operation.write({'state': 'to_approve'})
                    inventory_operation.message_post(body="sent to your admin to approve")
                else:
                    # 1. Filter orders that are currently in 'to_approve'
                    to_approve_orders = self.filtered(lambda inventory_operation: inventory_operation.state == 'to_approve')

                    # 2. Temporarily change their state to 'draft' WITHOUT tracking/chatter
                    if to_approve_orders:
                        to_approve_orders.with_context(tracking_disable=True).write({'state': 'draft'})

                    # 3. Call the standard Odoo confirm method on the whole recordset
                    # (Odoo will now see them as 'draft' and allow the confirmation)
                    return super(StockPicking, self).action_confirm()

        return True

    def button_validate(self):

        user_types = (self.env.user.internship_type or '').split(', ')
        is_intern_stock = self.env.user.is_intern and 'stock' in user_types



        for inventory_operation in self:

            if inventory_operation.state == 'to_approve' and is_intern_stock:
                inventory_operation.message_post(body="already sent to your admin to approve")

            else:
                if is_intern_stock:
                    inventory_operation.write({'state': 'to_approve'})
                    inventory_operation.message_post(body="sent to your admin to approve")
                else:
                    # 1. Filter orders that are currently in 'to_approve'
                    to_approve_orders = self.filtered(lambda inventory_operation: inventory_operation.state == 'to_approve')

                    # 2. Temporarily change their state to 'draft' WITHOUT tracking/chatter
                    if to_approve_orders:
                        to_approve_orders.with_context(tracking_disable=True).write({'state': 'draft'})

                    # 3. Call the standard Odoo confirm method on the whole recordset
                    # (Odoo will now see them as 'draft' and allow the confirmation)
                    return super(StockPicking, self).button_validate()

        return True
