from odoo import models,fields

class InheritedResConfig(models.TransientModel):
    _inherit='res.config.settings'

    module_stock_transport=fields.Boolean('Stock Transport')
