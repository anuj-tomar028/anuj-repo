from odoo import api,fields, models
import datetime
from odoo.exceptions import UserError

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "model created for specific use : Real_Estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    availability_date = fields.Date(copy=False,default=datetime.timedelta(3*365/12)+datetime.date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_areas = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        selection=[('north','North'), 
                   ('south','South'), 
                   ('east','East'), 
                   ('west','West')]
    )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    active=fields.Boolean(default=True)
    state=fields.Selection(
        selection=[('new','New'),
                   ('offer received','Offer received'),
                   ('offer accepted','Offer Accepted'),
                   ('sold','Sold'),
                   ('cancelled','Cancelled')],
        required=True,copy=False,default="new"
    )

    def action_do_sold(self):
        for property in self:
            if property.state == 'new':
                property.state = 'sold'
            elif property.state=='cancelled':
                raise UserError("Cannot mark as sold a property that is already cancelled.")
               
    def action_do_cancel(self):
        for property in self:
            if property.state == 'new':
                property.state = 'cancelled'
            elif property.state == 'sold':
                raise UserError("Cannot cancel a property that is already sold.")

    property_type_id=fields.Many2one("estate.property.type",string="Property Type")
    buyer_id=fields.Many2one('res.partner',string="Buyer",copy=False)
    salesperson_id=fields.Many2one(
        'res.users', 
        string='Salesperson', 
        default=lambda self: self.env.user.id
    )
    tag_ids=fields.Many2many("estate.property.tag",string="Tags")   

    total_area=fields.Float(compute="_compute_area",string="Total Area(sqm)")
    @api.depends('living_areas','garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area=record.living_areas+record.garden_area

    offer_ids = fields.One2many('estate.property.offer','property_id')
    best_price=fields.Float(compute="_compute_best_offer",string="Best Offer",store=True)
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(offer.price for offer in record.offer_ids)
            else:
                record.best_price = 0.0
