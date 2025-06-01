from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    konvergo_magic_auth_token = fields.Char(
        string="Konvergo Allo Auth Token",
        help="Authentication token used for Konvergo Allo integration"
    )
