from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):

    _name = "estate_property_offer"
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]
    _order = "price desc"

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

    #chapt 12 last part, this makes the offer linked to a property type when it is created
    property_type_id = fields.Many2one(
        "estate_property_type", related="property_id.property_type_id", string="Property Type", store=True
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # for computing of deadline and its inverse. used relativedelta for date arithmetic
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days



    #action methods for accepting and refusing offer 
    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer has already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted", 
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )
    
 