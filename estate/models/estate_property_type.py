from odoo import fields,models

class PropertyTypes(models.Model):
    _name="estate.property.type"
    _description="Estate Property Types"

    name=fields.Char()
