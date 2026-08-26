# -*- coding: utf-8 -*-
"""Job Costing Snapshot models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfJobCost(models.Model):
    _name = 'sf.job.cost'
    _description = 'Job Cost Snapshot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    job_name = fields.Char(string='Job / Project', required=True)
    snapshot_date = fields.Date(string='Snapshot', default=fields.Date.today)
    labor_cost = fields.Monetary(string='Labor')
    material_cost = fields.Monetary(string='Materials')
    overhead_cost = fields.Monetary(string='Overheads')
    budget_total = fields.Monetary(string='Budget')
    margin_percent = fields.Float(string='Margin %')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.job.cost') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.job.cost'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.job.cost'

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
