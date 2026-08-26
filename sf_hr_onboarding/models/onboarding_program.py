# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OnboardingTemplate(models.Model):
    _name = 'sf.onboarding.template'
    _description = 'Onboarding Template'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    program_type = fields.Selection([
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding'),
    ], string='Type', required=True)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')
    task_ids = fields.One2many('sf.onboarding.template.task',
                               'template_id', string='Tasks')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)


class OnboardingTemplateTask(models.Model):
    _name = 'sf.onboarding.template.task'
    _description = 'Onboarding Template Task'
    _order = 'sequence'

    template_id = fields.Many2one('sf.onboarding.template',
                                  string='Template',
                                  ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name', required=True)
    responsible_type = fields.Selection([
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('it', 'IT'),
        ('services', 'General Services'),
    ], string='Responsible', default='hr')
    offset_days = fields.Integer(string='Offset (days)', default=0)
    required = fields.Boolean(string='Required', default=True)
    category = fields.Selection([
        ('admin', 'Administration'),
        ('material', 'Material'),
        ('document', 'Document'),
        ('training', 'Training'),
        ('account', 'Account'),
        ('other', 'Other'),
    ], string='Category', default='admin')
    notes = fields.Text(string='Notes')


class OnboardingProgram(models.Model):
    _name = 'sf.onboarding.program'
    _description = 'Onboarding Program'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'key_date desc'

    name = fields.Char(string='Name', required=True,
                       default=lambda self: _('New'))
    program_type = fields.Selection([
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding'),
    ], string='Type', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    template_id = fields.Many2one('sf.onboarding.template',
                                  string='Template')
    key_date = fields.Date(string='Key Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    task_ids = fields.One2many('sf.onboarding.task', 'program_id',
                               string='Tasks')
    progress = fields.Float(string='Progress (%)',
                            compute='_compute_progress', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('task_ids.required', 'task_ids.state')
    def _compute_progress(self):
        for program in self:
            required = program.task_ids.filtered(lambda t: t.required)
            if required:
                done = required.filtered(lambda t: t.state == 'done')
                program.progress = round(len(done) / len(required) * 100,
                                         2)
            else:
                program.progress = 100.0

    def _generate_tasks(self):
        self.ensure_one()
        if not self.template_id:
            return
        vals_list = []
        for task in self.template_id.task_ids:
            vals = {
                'program_id': self.id,
                'sequence': task.sequence,
                'name': task.name,
                'category': task.category,
                'required': task.required,
                'notes': task.notes,
            }
            if self.key_date:
                from datetime import timedelta
                vals['due_date'] = self.key_date + timedelta(
                    days=task.offset_days)
            else:
                vals['due_date'] = fields.Date.today()
            responsible = self._map_responsible(task.responsible_type)
            if responsible:
                vals['responsible_id'] = responsible.id
            vals_list.append(vals)
        self.task_ids = [(0, 0, v) for v in vals_list]

    def _map_responsible(self, responsible_type):
        self.ensure_one()
        employee = self.employee_id
        if responsible_type == 'employee':
            return employee.user_id
        if responsible_type == 'manager':
            return employee.parent_id.user_id if employee.parent_id \
                else False
        groups = {
            'hr': 'hr.group_hr_manager',
            'it': 'base.group_system',
            'services': 'sf_hr_onboarding.group_hr_onboarding_manager',
        }
        if responsible_type in groups:
            group = self.env.ref(groups[responsible_type],
                                 raise_if_not_found=False)
            if group:
                return group.users[:1]
        return False

    def action_start(self):
        for program in self:
            if program.state != 'draft':
                raise UserError(_('Only draft programs can be started.'))
            program.state = 'in_progress'
            program.message_post(body=_('Program started.'))

    def action_complete(self):
        for program in self:
            if program.state != 'in_progress':
                raise UserError(
                    _('Only in-progress programs can be completed.'))
            open_required = program.task_ids.filtered(
                lambda t: t.required and t.state == 'open')
            if open_required:
                raise UserError(
                    _('All required tasks must be completed before '
                      'closing the program.'))
            program.state = 'completed'
            program.message_post(body=_('Program completed.'))

    def action_close(self):
        for program in self:
            if program.state != 'completed':
                raise UserError(
                    _('Only completed programs can be closed.'))
            program.state = 'closed'
            program.message_post(body=_('Program closed.'))

    def action_cancel(self):
        for program in self:
            if program.state not in ('draft', 'in_progress'):
                raise UserError(
                    _('Only draft or in-progress programs can be '
                      'cancelled.'))
            program.state = 'cancelled'
            program.message_post(body=_('Program cancelled.'))

    def unlink(self):
        for program in self:
            if program.state in ('in_progress', 'completed'):
                raise UserError(
                    _('An in-progress or completed program cannot be '
                      'deleted.'))
        return super().unlink()


class OnboardingTask(models.Model):
    _name = 'sf.onboarding.task'
    _description = 'Onboarding Task'
    _order = 'sequence'

    program_id = fields.Many2one('sf.onboarding.program',
                                 string='Program',
                                 ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name', required=True)
    category = fields.Selection([
        ('admin', 'Administration'),
        ('material', 'Material'),
        ('document', 'Document'),
        ('training', 'Training'),
        ('account', 'Account'),
        ('other', 'Other'),
    ], string='Category', default='admin')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('skipped', 'Skipped'),
    ], string='Status', default='open', tracking=True)
    required = fields.Boolean(string='Required', default=True)
    comments = fields.Text(string='Comments')
    material_prepared = fields.Boolean(string='Material Prepared')
    material_returned = fields.Boolean(string='Material Returned')
    completed_date = fields.Datetime(string='Completed Date')

    def action_start_task(self):
        for task in self:
            if task.state != 'open':
                raise UserError(_('Only open tasks can be started.'))
            task.state = 'in_progress'

    def action_mark_done(self):
        for task in self:
            if task.state not in ('open', 'in_progress'):
                raise UserError(
                    _('Only open or in-progress tasks can be done.'))
            task.state = 'done'
            task.completed_date = fields.Datetime.now()
            task.program_id.message_post(body=_(
                'Task "%s" completed.') % task.name)

    def action_skip(self):
        for task in self:
            if task.state != 'open':
                raise UserError(_('Only open tasks can be skipped.'))
            task.state = 'skipped'

    def action_mark_prepared(self):
        for task in self:
            task.material_prepared = True

    def action_mark_returned(self):
        for task in self:
            task.material_returned = True

    @api.model
    def _check_late_tasks(self):
        today = fields.Date.today()
        late = self.search([
            ('state', 'in', ('open', 'in_progress')),
            ('due_date', '!=', False),
            ('due_date', '<', today),
        ])
        for task in late:
            if task.responsible_id:
                existing = task.activity_ids.filtered(
                    lambda a: a.summary ==
                    _('Late onboarding task: %s') % task.name)
                if not existing:
                    task.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Late onboarding task: %s') % task.name,
                        note=_('The task "%s" is overdue since %s.') % (
                            task.name, task.due_date),
                        user_id=task.responsible_id.id,
                        date_deadline=task.due_date,
                    )