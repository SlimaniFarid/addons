# -*- coding: utf-8 -*-
"""Safety Training Compliance models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSafety_training_tracker(models.Model):
    _name = 'sf.safety_training_tracker'
    _description = 'Safety Training Compliance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    training_type = fields.Selection([
        ('fire', 'Fire Safety'),
        ('first_aid', 'First Aid'),
        ('forklift', 'Forklift'),
        ('chemical', 'Chemical Handling'),
        ('other', 'Other'),
        ], string='Training', required=True)
    completed_date = fields.Date(string='Completed')
    expiry_date = fields.Date(string='Expiry')
    compliant = fields.Boolean(string='Compliant')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.safety_training_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.safety_training_tracker'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
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

    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

