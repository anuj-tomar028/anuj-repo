from odoo import fields,models

class PropertyTypes(models.Model):
    _name="estate.property.type"
    _description="Estate Property Types"

    name=fields.Char()
    property_ids=fields.One2many('estate.property','property_type_id')
