from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):

    _name = "estate_property_offer"
    _description = "Real Estate Property Offer"

    price = fields.Float("Price", required=True)

    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    #relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)

    property_type_id = fields.Many2one(
        "estate_property_type", related="property_id.property_type_id", string="Property Type", store=True
    )