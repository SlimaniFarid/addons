# -*- coding: utf-8 -*-
"""Pipeline Hygiene Audit models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPipelineAudit(models.Model):
    _name = 'sf.pipeline.audit'
    _description = 'Pipeline Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    audit_date = fields.Date(string='Audit Date', required=True, default=fields.Date.today)
    stale_opportunities = fields.Integer(string='Stale Opportunities')
    missing_next_step = fields.Integer(string='Missing Next Step')
    overdue_close = fields.Integer(string='Overdue Close Dates')
    cleanup_campaign = fields.Html(string='Cleanup Campaign')
    auditor_id = fields.Many2one('res.users', string='Auditor')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('actions', 'Actions Assigned'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.pipeline.audit') or 'NEW'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_actions(self):
        self.write({'state': 'actions'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.pipeline.audit'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.pipeline.audit'

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
