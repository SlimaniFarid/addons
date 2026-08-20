# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class OhMedicalFile(models.Model):
    _name = 'sf.oh.medical.file'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Occupational Health File'
    _order = 'employee_id, id'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True, ondelete='cascade',
                                  index=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    ], string='Status', default='active', required=True, tracking=True)
    visit_ids = fields.One2many('sf.oh.visit', 'medical_file_id',
                                string='Visits')
    exposure_ids = fields.Many2many('sf.oh.exposure',
                                    string='Exposures')
    restriction_ids = fields.One2many('sf.oh.restriction',
                                      'medical_file_id',
                                      string='Restrictions')
    vaccination_ids = fields.One2many('sf.oh.vaccination',
                                      'medical_file_id',
                                      string='Vaccinations')
    last_aptitude = fields.Selection([
        ('apt', 'Fit'),
        ('apt_restricted', 'Fit with restrictions'),
        ('inapt', 'Unfit'),
    ], string='Last aptitude', compute='_compute_from_visits', store=True)
    last_visit_date = fields.Date(string='Last visit date',
                                  compute='_compute_from_visits', store=True)
    next_due_date = fields.Date(string='Next due date',
                                compute='_compute_from_visits', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('employee_uniq', 'UNIQUE(employee_id)',
         _('This employee already has an occupational health file.')),
    ]

    @api.depends('visit_ids.state', 'visit_ids.result',
                 'visit_ids.done_date', 'visit_ids.planned_date',
                 'visit_ids.validity_to')
    def _compute_from_visits(self):
        today = fields.Date.today()
        for file in self:
            done = file.visit_ids.filtered(lambda v: v.state == 'done')
            last = done.sorted(key=lambda v: v.done_date or v.planned_date,
                               reverse=True)[:1]
            file.last_aptitude = last.result if last else False
            file.last_visit_date = last.done_date if last else False
            upcoming = file.visit_ids.filtered(
                lambda v: v.state in ('planned', 'scheduled')
                and v.planned_date and v.planned_date >= today)
            next_due = upcoming.sorted(key=lambda v: v.planned_date)[:1].planned_date
            if not next_due and last and last.validity_to:
                next_due = last.validity_to
            file.next_due_date = next_due or False

    def action_suspend(self):
        self.ensure_one()
        self.state = 'suspended'

    def action_reactivate(self):
        self.ensure_one()
        self.state = 'active'

    def action_close(self):
        self.ensure_one()
        if self.visit_ids.filtered(lambda v: v.state in ('draft', 'planned', 'scheduled')):
            raise UserError(_('Close all open visits before closing the file.'))
        self.state = 'closed'

    def unlink(self):
        for file in self:
            if file.state == 'active':
                raise UserError(_('An active medical file cannot be deleted. '
                                  'Archive or close it first.'))
        return super().unlink()

    def _check_oh_expiry_alerts(self):
        today = fields.Date.today()
        for file in self.search([('state', '=', 'active')]):
            if not file.next_due_date:
                continue
            window = file.company_id.sf_oh_alert_days
            days_left = (file.next_due_date - today).days
            if 0 <= days_left <= window:
                manager = self.env['res.users'].search([
                    ('groups_id', 'in', self.env.ref('sf_occupational_health.group_oh_manager').id),
                    ('share', '=', False),
                ], limit=1)
                if manager:
                    file.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Medical visit due for %s')
                        % file.employee_id.name,
                        note=_('The aptitude for %s expires on %s.')
                        % (file.employee_id.name, file.next_due_date),
                        user_id=manager.id)
            if file.company_id.sf_oh_auto_create_periodic and 0 <= days_left <= window:
                existing = file.visit_ids.filtered(
                    lambda v: v.state in ('draft', 'planned', 'scheduled'))
                if not existing:
                    self.env['sf.oh.visit'].create({
                        'medical_file_id': file.id,
                        'visit_type': 'periodic',
                        'planned_date': file.next_due_date,
                    })


class OhVisit(models.Model):
    _name = 'sf.oh.visit'
    _description = 'Medical Visit'
    _order = 'planned_date desc, id desc'

    medical_file_id = fields.Many2one('sf.oh.medical.file',
                                      string='Medical file', required=True,
                                      ondelete='cascade', index=True)
    visit_type = fields.Selection([
        ('hire', 'Hire'),
        ('periodic', 'Periodic'),
        ('reprise', 'Return to work'),
        ('follow_up', 'Follow-up'),
        ('exposure', 'Exposure'),
        ('other', 'Other'),
    ], string='Type', required=True, default='periodic')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True)
    doctor_id = fields.Many2one('sf.oh.doctor', string='Doctor',
                                ondelete='restrict')
    planned_date = fields.Date(string='Planned date', index=True)
    done_date = fields.Date(string='Done date')
    result = fields.Selection([
        ('apt', 'Fit'),
        ('apt_restricted', 'Fit with restrictions'),
        ('inapt', 'Unfit'),
    ], string='Result')
    restriction_note = fields.Text(string='Restriction note')
    validity_from = fields.Date(string='Validity start')
    validity_to = fields.Date(string='Validity end', index=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='medical_file_id.company_id',
                                 store=True, readonly=True)

    @api.constrains('state', 'result')
    def _check_result(self):
        for visit in self:
            if visit.state == 'done' and not visit.result:
                raise ValidationError(_('A medical result is required to '
                                        'mark the visit as done.'))

    @api.constrains('validity_from', 'validity_to')
    def _check_validity(self):
        for visit in self:
            if (visit.validity_from and visit.validity_to
                    and visit.validity_to < visit.validity_from):
                raise ValidationError(_('The validity end date cannot be '
                                        'before the validity start date.'))

    def action_plan(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft visits can be planned.'))
        if not self.planned_date:
            self.planned_date = fields.Date.context_today(self)
        self.state = 'planned'

    def action_schedule(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned visits can be scheduled.'))
        return {
            'name': _('Schedule Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.oh.schedule.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_visit_id': self.id},
        }

    def action_record_result(self):
        self.ensure_one()
        if self.state not in ('planned', 'scheduled'):
            raise UserError(_('Only planned or scheduled visits can be '
                              'recorded.'))
        return {
            'name': _('Record Visit Result'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.oh.visit.result.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_visit_id': self.id},
        }

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('done', 'closed', 'cancelled'):
            raise UserError(_('This visit cannot be cancelled.'))
        self.state = 'cancelled'

    def action_close(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only done visits can be closed.'))
        self.state = 'closed'


class OhDoctor(models.Model):
    _name = 'sf.oh.doctor'
    _description = 'Occupational Health Doctor'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Practice')
    license_number = fields.Char(string='License number')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', _('This doctor already exists.')),
    ]


class OhExposure(models.Model):
    _name = 'sf.oh.exposure'
    _description = 'Exposure Reason'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    standard_interval_months = fields.Integer(
        string='Default periodicity (months)', default=12)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This exposure reason already exists.')),
    ]


class OhRestriction(models.Model):
    _name = 'sf.oh.restriction'
    _description = 'Medical Restriction'

    medical_file_id = fields.Many2one('sf.oh.medical.file',
                                      string='Medical file', required=True,
                                      ondelete='cascade', index=True)
    name = fields.Char(string='Name', required=True)
    incompatible_work = fields.Text(string='Incompatible work')
    effective_from = fields.Date(string='Effective from')
    effective_to = fields.Date(string='Effective to')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='medical_file_id.company_id',
                                 store=True, readonly=True, index=True)


class OhVaccination(models.Model):
    _name = 'sf.oh.vaccination'
    _description = 'Employee Vaccination'

    medical_file_id = fields.Many2one('sf.oh.medical.file',
                                      string='Medical file', required=True,
                                      ondelete='cascade', index=True)
    name = fields.Char(string='Vaccine', required=True)
    dose = fields.Char(string='Dose', help='e.g. 2/3')
    administered_on = fields.Date(string='Administered on')
    next_due = fields.Date(string='Next due')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='medical_file_id.company_id',
                                 store=True, readonly=True, index=True)


class OhScheduleWizard(models.TransientModel):
    _name = 'sf.oh.schedule.wizard'
    _description = 'Schedule Medical Visit'

    visit_id = fields.Many2one('sf.oh.visit', string='Visit', required=True)
    doctor_id = fields.Many2one('sf.oh.doctor', string='Doctor')
    planned_date = fields.Date(string='Planned date',
                               default=lambda self: fields.Date.context_today(self),
                               required=True)

    def action_confirm(self):
        self.ensure_one()
        self.visit_id.write({
            'doctor_id': self.doctor_id.id,
            'planned_date': self.planned_date,
            'state': 'scheduled',
        })
        return {'type': 'ir.actions.act_window_close'}


class OhVisitResultWizard(models.TransientModel):
    _name = 'sf.oh.visit.result.wizard'
    _description = 'Record Visit Result'

    visit_id = fields.Many2one('sf.oh.visit', string='Visit', required=True)
    result = fields.Selection([
        ('apt', 'Fit'),
        ('apt_restricted', 'Fit with restrictions'),
        ('inapt', 'Unfit'),
    ], string='Result', required=True)
    restriction_note = fields.Text(string='Restriction note')
    validity_from = fields.Date(string='Validity start')
    validity_to = fields.Date(string='Validity end')
    create_restriction = fields.Boolean(
        string='Create a restriction', default=False)
    restriction_name = fields.Char(string='Restriction name')

    @api.constrains('validity_from', 'validity_to')
    def _check_validity(self):
        for wizard in self:
            if (wizard.validity_from and wizard.validity_to
                    and wizard.validity_to < wizard.validity_from):
                raise ValidationError(_('The validity end date cannot be '
                                        'before the validity start date.'))

    def action_confirm(self):
        self.ensure_one()
        visit = self.visit_id
        visit.write({
            'result': self.result,
            'restriction_note': self.restriction_note,
            'validity_from': self.validity_from,
            'validity_to': self.validity_to,
            'done_date': fields.Date.context_today(self),
            'state': 'done',
        })
        if self.create_restriction:
            self.env['sf.oh.restriction'].create({
                'medical_file_id': visit.medical_file_id.id,
                'name': self.restriction_name or _('Restriction'),
                'incompatible_work': self.restriction_note,
                'effective_from': self.validity_from,
                'effective_to': self.validity_to,
            })
        return {'type': 'ir.actions.act_window_close'}