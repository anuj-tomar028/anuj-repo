from datetime import timedelta
from odoo import api,fields,models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate property Offers"

    price=fields.Float()
    status=fields.Selection(
        selection=[('draft','Draft'),
                   ('accepted','Accepted'),
                   ('refused','Refused')],
        copy=False,string="Status",default='draft'
    )       
    partner_id = fields.Many2one('res.partner', string = 'Partner',required = False,  default=lambda self: self.env.user)
    property_id = fields.Many2one('estate.property', default=lambda self: self.env.user)
    create_date=fields.Date(default=lambda self: fields.Date.today(),invisible=True)
    validity=fields.Integer(default=7,string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline",string="Deadline Date")
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
                
    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = 7
 
    def action_accept_offer(self):
        for offer in self:
            if offer.status == 'draft':
                offer.status = 'accepted'
                offer.property_id.buyer_id=offer.partner_id
                offer.property_id.selling_price=offer.price
                other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id)])
                other_offers.write({'status': 'refused'})
                
    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'draft':
                offer.status = 'refused'
