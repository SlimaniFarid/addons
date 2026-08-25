# -*- coding: utf-8 -*-
"""Customer Feedback Action Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFeedbackAction(models.Model):
    _name = 'sf.feedback.action'
    _description = 'Feedback Action'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    feedback_summary = fields.Text(string='Feedback Summary', required=True)
    source = fields.Selection([
        ('survey', 'Survey'),
        ('meeting', 'Meeting'),
        ('complaint', 'Complaint'),
        ('review', 'Review'),
        ], string='Source', required=True, default=meeting)
    action = fields.Text(string='Action Committed', required=True)
    owner_id = fields.Many2one('res.users', string='Owner')
    due_date = fields.Date(string='Due Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('customer_validated', 'Customer Validated'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.feedback.action') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_customer_validated(self):
        self.write({'state': 'customer_validated'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.feedback.action'

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

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

