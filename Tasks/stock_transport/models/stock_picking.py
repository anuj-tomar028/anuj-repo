from odoo import api,models, fields

class TransferBatch(models.Model):
    _inherit = 'stock.picking'

    volume=fields.Float()
