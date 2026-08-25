# -*- coding: utf-8 -*-
"""Sales Hiring & Ramp Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_hiring_tracker(models.Model):
    _name = 'sf.sales_hiring_tracker'
    _description = 'Sales Hiring & Ramp Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    candidate_name = fields.Char(string='Candidate', required=True)
    stage = fields.Selection([
        ('sourcing', 'Sourcing'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('ramping', 'Ramping'),
        ('productive', 'Productive'),
        ], string='Stage', required=True)
    start_date = fields.Date(string='Start Date')
    ramp_end_date = fields.Date(string='Ramp End')
    quota_attainment = fields.Float(string='Quota Attainment %')
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
                    'sf.sales_hiring_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.sales_hiring_tracker'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('ramp_end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.ramp_end_date
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
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.ramp_end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

