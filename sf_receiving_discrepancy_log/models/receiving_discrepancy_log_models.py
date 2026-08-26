# -*- coding: utf-8 -*-
"""Goods Receipt Discrepancy Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfReceiptDiscrepancy(models.Model):
    _name = 'sf.receipt.discrepancy'
    _description = 'Receipt Discrepancy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    picking_id = fields.Many2one('stock.picking', string='Receipt', required=True)
    discrepancy_type = fields.Selection([
        ('shortage', 'Quantity Shortage'),
        ('damage', 'Damage'),
        ('wrong_item', 'Wrong Item'),
        ('other', 'Other'),
        ], string='Type', required=True)
    qty_affected = fields.Float(string='Qty Affected')
    disposition = fields.Selection([
        ('accept', 'Accept with Deduction'),
        ('return', 'Return to Vendor'),
        ('claim', 'Claim'),
        ], string='Disposition', default=accept)
    supplier_notified = fields.Boolean(string='Supplier Notified')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('notified', 'Notified'),
        ('resolved', 'Resolved'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.receipt.discrepancy') or 'NEW'
        return super().create(vals_list)

    def action_notified(self):
        self.write({'state': 'notified'})

    def action_resolved(self):
        self.write({'state': 'resolved'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.receipt.discrepancy'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.receipt.discrepancy'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
