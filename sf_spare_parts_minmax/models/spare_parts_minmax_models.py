# -*- coding: utf-8 -*-
"""Spare Parts Min/Max models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class SfSparePart(models.Model):
    _name = 'sf.spare.part'
    _description = 'Spare Part Parameter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Spare Part', required=True)
    criticality = fields.Selection([
        ('critical', 'Critical - Stopper'),
        ('important', 'Important'),
        ('standard', 'Standard'),
        ], string='Criticality', required=True, default=important)
    min_qty = fields.Float(string='Min Qty')
    max_qty = fields.Float(string='Max Qty')
    lead_time_days = fields.Integer(string='Lead Time (days)')
    supplier_ref = fields.Char(string='Supplier Ref')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('review', 'Under Review'),
        ('archived', 'Archived'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.spare.part') or 'NEW'
        return super().create(vals_list)

    def action_review(self):
        self.write({'state': 'review'})

    def action_archived(self):
        self.write({'state': 'archived'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.spare.part'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.spare.part'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
