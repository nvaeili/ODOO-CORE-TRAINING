from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Real Estate Property Tag"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name of the Tag must be unique"),
    ]
    _order = "name"

    # Fields Declaration
    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index")
