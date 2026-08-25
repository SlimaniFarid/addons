# -*- coding: utf-8 -*-
"""Financial close checklist models."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCloseTemplate(models.Model):
    _name = 'sf.close.template'
    _description = 'Close Checklist Template'

    name = fields.Char(string='Template Name', required=True)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)
    step_ids = fields.One2many('sf.close.template.step', 'template_id',
                               string='Steps', copy=True)


class SfCloseTemplateStep(models.Model):
    _name = 'sf.close.template.step'
    _description = 'Close Template Step'
    _order = 'sequence, id'

    template_id = fields.Many2one('sf.close.template', required=True,
                                  ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Task', required=True)
    department = fields.Selection([
        ('accounting', 'Accounting'), ('treasury', 'Treasury'),
        ('purchasing', 'Purchasing'), ('sales', 'Sales'),
        ('inventory', 'Inventory'), ('hr', 'HR'), ('it', 'IT'),
        ('management', 'Management')], required=True, default='accounting')
    due_offset_days = fields.Integer(
        string='Due (days after period end)', default=1)
    description = fields.Text(string='Instructions')


class SfClosePeriod(models.Model):
    _name = 'sf.close.period'
    _description = 'Close Period'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc'

    name = fields.Char(string='Period', required=True, copy=False,
                       readonly=True, default='New')
    date_start = fields.Date(string='Period Start', required=True)
    date_end = fields.Date(string='Period End', required=True)
    template_id = fields.Many2one('sf.close.template',
                                  string='Checklist Template', required=True)
    responsible_id = fields.Many2one('res.users', string='Close Owner')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    task_ids = fields.One2many('sf.close.task', 'period_id', string='Tasks')
    task_count = fields.Integer(compute='_compute_stats')
    done_count = fields.Integer(compute='_compute_stats')
    blocked_count = fields.Integer(compute='_compute_stats')
    progress_percent = fields.Float(compute='_compute_stats')
    state = fields.Selection([
        ('draft', 'Draft'), ('in_progress', 'In Progress'),
        ('blocked', 'Blocked'), ('closed', 'Closed'), ('cancelled',
                                                     'Cancelled')],
        default='draft', tracking=True)
    closed_date = fields.Date(string='Closed On', readonly=True)
    signed_off_by_id = fields.Many2one('res.users', string='Signed Off By',
                                       readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.close.period') or 'CLOSE-NEW'
        return super().create(vals_list)

    def _compute_stats(self):
        for rec in self:
            tasks = rec.task_ids
            applicable = tasks.filtered(lambda t: t.state != 'na')
            done = applicable.filtered(lambda t: t.state == 'done')
            rec.task_count = len(tasks)
            rec.done_count = len(done)
            rec.blocked_count = len(tasks.filtered(lambda t: t.state ==
                                                   'blocked'))
            rec.progress_percent = (len(done) / len(applicable) * 100.0
                                    if applicable else 0.0)

    def action_start(self):
        self.ensure_one()
        if self.task_ids:
            raise UserError(_('Tasks already generated.'))
        vals_list = [{
            'period_id': self.id,
            'sequence': step.sequence,
            'name': step.name,
            'department': step.department,
            'due_date': self.date_end + rd.relativedelta(
                days=step.due_offset_days),
            'description': step.description,
        } for step in self.template_id.step_ids]
        self.env['sf.close.task'].create(vals_list)
        self.write({'state': 'in_progress'})

    def action_close(self):
        self.ensure_one()
        blocking = self.task_ids.filtered(
            lambda t: t.state not in ('done', 'na'))
        if blocking:
            raise UserError(_('%s tasks are not Done/NA: %s') % (
                len(blocking), ', '.join(blocking.mapped('name')[:5])))
        self.write({'state': 'closed', 'closed_date': fields.Date.today(),
                    'signed_off_by_id': self.env.uid})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfCloseTask(models.Model):
    _name = 'sf.close.task'
    _description = 'Close Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period_id, sequence, id'

    period_id = fields.Many2one('sf.close.period', string='Close Period',
                                required=True, ondelete='cascade')
    company_id = fields.Many2one(related='period_id.company_id', store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Task', required=True)
    department = fields.Selection([
        ('accounting', 'Accounting'), ('treasury', 'Treasury'),
        ('purchasing', 'Purchasing'), ('sales', 'Sales'),
        ('inventory', 'Inventory'), ('hr', 'HR'), ('it', 'IT'),
        ('management', 'Management')], required=True, default='accounting')
    due_date = fields.Date(string='Due Date')
    description = fields.Text(string='Instructions')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    state = fields.Selection([
        ('pending', 'Pending'), ('in_progress', 'In Progress'),
        ('done', 'Done'), ('blocked', 'Blocked'), ('na', 'N/A')],
        default='pending', tracking=True)
    done_date = fields.Date(string='Completed On', readonly=True)
    blocker_note = fields.Text(string='Blocker / Comment')
    signed_off_by_id = fields.Many2one('res.users', string='Signed Off By',
                                       readonly=True)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        for rec in self:
            rec.write({'state': 'done', 'done_date': fields.Date.today(),
                       'signed_off_by_id': rec.env.uid})

    def action_block(self):
        for rec in self:
            if not rec.blocker_note:
                raise UserError(_('Describe the blocker before flagging.'))
            rec.write({'state': 'blocked'})
            rec.period_id.sudo().write({'state': 'blocked'})

    def action_na(self):
        self.write({'state': 'na'})

    def action_reset(self):
        self.write({'state': 'pending', 'done_date': False})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.close.template'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
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
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

