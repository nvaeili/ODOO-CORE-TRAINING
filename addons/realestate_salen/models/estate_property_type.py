from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name of the Type must be unique"),
    ]
    _order = "name, sequence"

    # Fields Declaration
    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")
    property_ids = fields.One2many("estate_property", "property_type_id", string="Properties")

    # Last part of chapter 12
    offer_ids = fields.Many2many("estate_property_offer", string="Offers", compute="_compute_offer")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")

    # Computation Method
    def _compute_offer(self):
        # Using read_group to gather offer data based on certain conditions
        data = self.env["estate_property_offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)],
            ["ids:array_agg(id)", "property_type_id"],
            ["property_type_id"],
        )
        # Mapping offer counts and IDs based on property type
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    # Action Method
    def action_view_offers(self):
        # Retrieving offers associated with the property type
        res = self.env.ref("realestate_salen.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res
