# -*- coding: utf-8 -*-
"""Cycle Count Scheduler models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCycleCount(models.Model):
    _name = 'sf.cycle.count'
    _description = 'Cycle Count'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    zone = fields.Char(string='Zone / Location', required=True)
    abc_class = fields.Selection([
        ('a', 'A - High Value'),
        ('b', 'B'),
        ('c', 'C - Low Value'),
        ], string='ABC Class', default=b)
    scheduled_date = fields.Date(string='Scheduled', required=True)
    counted_lines = fields.Integer(string='Lines Counted')
    variance_lines = fields.Integer(string='Variance Lines')
    counter_id = fields.Many2one('res.users', string='Counter')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('counted', 'Counted'),
        ('approved', 'Approved'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.cycle.count') or 'NEW'
        return super().create(vals_list)

    def action_counted(self):
        self.write({'state': 'counted'})

    def action_approved(self):
        self.write({'state': 'approved'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.cycle.count'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.cycle.count'

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
