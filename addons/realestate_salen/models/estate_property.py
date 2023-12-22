from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real Estate Salen"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]
    _order = "id desc"

    name = fields.Char(string='Title',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode',)


    #using Date.today() to get date today 
    date_availability = fields.Date(string='Date Availability', copy=False, months=3, default=lambda self: fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(string='Expected Price', require=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [('N', 'North'), 
         ('S', 'South'), 
         ('Et', 'East'), 
         ('W', 'West')],
        string='Garden Orientation'
    )
    active = fields.Boolean(default=True)
    #state field that has 5 values possible.
    state = fields.Selection(
            [('new', 'New'),
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')],
            string='Status',
            require=True,
            copy=False,
            default='new')
    
    # for relational
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")

    # defining total area & best price 
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )

    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    # Computing the total area & best price 
    # "prop" is used as a reference to each indiv record with the collection 'self'

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    #using max for maximum offer 
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    #using onchange()  
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        return super().unlink()

    # defining the action
    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
    


    #adding sql constraints so that the selling price cannot be lower than 90% of the expected price.
    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )