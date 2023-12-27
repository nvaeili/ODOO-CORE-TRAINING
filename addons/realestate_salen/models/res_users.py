from odoo import fields, models

class ResUsers(models.Model):


    _inherit = "res.users"

    # Relational (added a domain so that it only lists the available properties)
    property_ids = fields.One2many(
        "estate_property", "user_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])]
    )