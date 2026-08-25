# -*- coding: utf-8 -*-
"""External Audit Finding Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAuditFinding(models.Model):
    _name = 'sf.audit.finding'
    _description = 'Audit Finding'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    audit_ref = fields.Char(string='Audit Reference', required=True)
    finding = fields.Text(string='Finding', required=True)
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('observation', 'Observation'),
        ], string='Severity', required=True)
    owner_id = fields.Many2one('res.users', string='Remediation Owner', required=True)
    due_date = fields.Date(string='Remediation Due')
    evidence = fields.Html(string='Closure Evidence')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_remediation', 'In Remediation'),
        ('pending_verification', 'Pending Verification'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.audit.finding') or 'NEW'
        return super().create(vals_list)

    def action_in_remediation(self):
        self.write({'state': 'in_remediation'})

    def action_pending_verification(self):
        self.write({'state': 'pending_verification'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.audit.finding'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

