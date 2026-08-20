# -*- coding: utf-8 -*-
from odoo import fields, models, _


class StockPickingExt(models.Model):
    _inherit = 'stock.picking'

    sf_wave_id = fields.Many2one('sf.wave.picking', string='Wave',
                                 ondelete='set null')