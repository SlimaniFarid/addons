# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SlottingResult(models.Model):
    _name = 'sf.warehouse.heatmap.slotting.result'
    _description = 'Slotting Result'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    analysis_id = fields.Many2one(comodel_name='sf.warehouse.heatmap.slotting.analysis', ondelete='restrict')
    product_id = fields.Many2one(comodel_name='product.product', ondelete='restrict')
    pick_count = fields.Integer(string='Pick Count')
    current_location = fields.Char(string='Current Location')
    abc_class = fields.Selection([
        ('A', 'Class A'), ('B', 'Class B'), ('C', 'Class C'),
        ], string='ABC Class', default='C')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.warehouse.heatmap.slotting.analysis'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

