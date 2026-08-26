# -*- coding: utf-8 -*-
"""Employee 1-on-1 Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEmployee_1on1_tracker(models.Model):
    _name = 'sf.employee_1on1_tracker'
    _description = 'Employee 1-on-1 Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    manager_id = fields.Many2one('res.users', string='Manager')
    meeting_date = fields.Date(string='Meeting Date', default=fields.Date.today)
    topics = fields.Text(string='Topics Discussed')
    mood = fields.Selection([
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
        ], string='Mood', default=neutral)
    actions = fields.Text(string='Development Actions')
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
                    'sf.employee_1on1_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.employee_1on1_tracker'

    active = fields.Boolean(string='Active', default=True)
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave2 ---
class _Wave21on1(models.Model):
    _inherit = 'sf.employee_1on1_tracker'

    @api.model
    def cron_scan_overdue(self):
        """Create a draft 1:1 for every active employee whose manager has
        no record within the cadence (default 30 days)."""
        Employee = self.env['hr.employee']
        cadence_days = 30
        cutoff = fields.Date.context_today(self) - relativedelta(
            days=cadence_days)
        employees = Employee.search([('active', '=', True)])
        created = 0
        for emp in employees:
            if not emp.parent_id:
                continue
            recent = self.search([
                ('employee_id', '=', emp.id),
                ('manager_id', '=', emp.parent_id.id),
                ('meeting_date', '>=', cutoff)], limit=1)
            if recent:
                continue
            self.create({
                'employee_id': emp.id,
                'manager_id': emp.parent_id.id,
                'meeting_date': fields.Date.context_today(self),
                'topics': _('Periodic check-in auto-created by scanner.'),
            })
            created += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('1:1 scanner'),
                       'message': _('%s overdue 1:1 drafted.') % created,
                       'type': 'success'},
        }
