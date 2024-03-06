from odoo import api,models,fields
import datetime

class PickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    vehicle_category_id=fields.Many2one(related="vehicle_id.category_id", readonly=True, copy=False)
    doc=fields.Many2one('dock')
    move_ids= fields.One2many("stock.move", string="Stock Moves", compute='_compute_move_ids',search=True)
    date_end= fields.Date('End date',copy=False, default=lambda self:(datetime.date.today()+datetime.timedelta(days=7)))
    transfer=fields.Float(string="Transfer",store=True)
    lines=fields.Float(string="Lines",store=True)
    total_weight = fields.Float(compute='_compute_weight', string="Weight")
    total_volume = fields.Float(compute='_compute_volume', string="Volume")   
     
    @api.depends('move_ids.product_id','move_ids.quantity')
    def _compute_weight(self):
        for batch in self:
            total_weight = 0.0
            for move in batch.move_ids:
                total_weight += move.product_id.weight * move.quantity
            batch.total_weight = total_weight
            max_weight = batch.vehicle_category_id.max_weight
            if max_weight:
                batch.total_weight = (total_weight / max_weight)*100
            else:
                batch.total_weight = 0.0
   
    @api.depends('move_ids.product_id','move_ids.quantity')
    def _compute_weight(self):
        for batch in self:
            total_volume = 0.0
            for move in batch.move_ids:
                total_volume += move.product_id.volume * move.quantity
            batch.total_volume = total_volume
            max_volume = batch.vehicle_category_id.max_volume
            if max_volume:
                batch.total_volume = (total_volume / max_volume)*100
            else:
                batch.total_volume = 0.0
