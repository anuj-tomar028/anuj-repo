from odoo import models, fields

class Doc(models.Model):
    _name = 'dock'

    name=fields.Char('Name')
