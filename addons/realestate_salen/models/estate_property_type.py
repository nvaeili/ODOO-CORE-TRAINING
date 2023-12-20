from odoo import models, fields

class EstatePropertyType(models.Model):

    _name = "estate_property_type"
    _description = "Real Estate Property Type"

    name = fields.Char("Name", required=True)

    property_ids = fields.One2many("estate_property", "property_type_id", string="Properties")