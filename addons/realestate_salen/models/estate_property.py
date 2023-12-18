from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real Estate Salen"

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode',)
    #using Date.today() to get date today 
    date_availability = fields.Date(string='Date Availability', copy=False, months=3, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', require=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        [('north', 'North'), 
         ('south', 'South'), 
         ('east', 'East'), 
         ('west', 'West')],
        string='Garden Orientation'
    )
    active = fields.Boolean(default=True)
    #state field that has 5 values possible.
    state = fields.Selection(
            [('new', 'New'),
            ('offer received', 'Offer received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')],
            string='State',
            require=True,
            copy=False,
            default='new')