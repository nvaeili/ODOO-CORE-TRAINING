from odoo import models, fields

class EstatePropertyType(models.Model):
        
    _name = "estate_property_tag"
    _description = "Real Estate Property Tag"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color Index")