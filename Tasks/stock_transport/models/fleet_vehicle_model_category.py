from odoo import models, fields, api

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Integer(string='Max Weight (kgs)')
    max_volume = fields.Integer(string='Max Volume')

    @api.depends('name','max_weight','max_volume')
    def _compute_display_name(self):
        for record in self:
            record.display_name = "{} ({} kg, {} m3)".format(record.name, record.max_weight,record.max_volume)
