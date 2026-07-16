from odoo import api, fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    is_intern = fields.Boolean(
        string="Intern",
        compute="_compute_internship_data",
        store=True,
    )

    internship_type = fields.Char(
        string="Internship Type",
        compute="_compute_internship_data",
        store=True,
    )

    @api.depends('groups_id')
    def _compute_internship_data(self):
        sale_group = self.env.ref('internship_app.group_intern_sale', raise_if_not_found=False)
        purchase_group = self.env.ref('internship_app.group_intern_purchase', raise_if_not_found=False)
        stock_group = self.env.ref('internship_app.group_intern_stock', raise_if_not_found=False)
        account_group = self.env.ref('internship_app.group_intern_account', raise_if_not_found=False)

        for user in self:
            internship_types = []
            if sale_group and sale_group in user.groups_id:
                internship_types.append('sale')
            if purchase_group and purchase_group in user.groups_id:
                internship_types.append('purchase')
            if stock_group and stock_group in user.groups_id:
                internship_types.append('stock')
            if account_group and account_group in user.groups_id:
                internship_types.append('account')

            user.is_intern = bool(internship_types)
            user.internship_type = ', '.join(internship_types) if internship_types else False