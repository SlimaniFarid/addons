# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVeterinaryVaccination(models.Model):
    _name = 'sf.veterinary.vaccination'
    _description = 'Veterinary Vaccination'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    patient_id = fields.Many2one(
        'sf.veterinary.patient', string='Patient', ondelete='restrict',
        required=True, index=True, tracking=True)
    vaccine_name = fields.Char(string='Vaccine', required=True, tracking=True)
    dose_number = fields.Integer(string='Dose number', default=1,
                                 tracking=True)
    administered_date = fields.Date(
        string='Administered date', default=fields.Date.context_today,
        tracking=True)
    next_due_date = fields.Date(
        string='Next due date', compute='_compute_next_due_date', store=True,
        readonly=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('administered', 'Administered'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('administered_date', 'company_id',
                 'company_id.sf_veterinary_vaccination_due_days')
    def _compute_next_due_date(self):
        for vaccination in self:
            if vaccination.administered_date:
                vaccination.next_due_date = vaccination.administered_date + \
                    timedelta(days=vaccination.company_id.sf_veterinary_vaccination_due_days)
            else:
                vaccination.next_due_date = False

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.veterinary.vaccination')
        if not vals.get('patient_id'):
            raise UserError(_('A vaccination requires a patient.'))
        self._check_duplicate(vals)
        return super().create(vals)

    def write(self, vals):
        if vals.get('patient_id') is False:
            raise UserError(_('A vaccination requires a patient.'))
        if 'patient_id' in vals or 'vaccine_name' in vals:
            for vaccination in self:
                check_vals = dict(vals)
                check_vals['id'] = vaccination.id
                if not check_vals.get('patient_id'):
                    check_vals['patient_id'] = vaccination.patient_id.id
                if not check_vals.get('vaccine_name'):
                    check_vals['vaccine_name'] = vaccination.vaccine_name
                self._check_duplicate(check_vals)
        return super().write(vals)

    def _check_duplicate(self, vals):
        if not vals.get('patient_id') or not vals.get('vaccine_name'):
            return
        today = fields.Date.context_today(self)
        existing = self.search([
            ('patient_id', '=', vals['patient_id']),
            ('vaccine_name', '=', vals['vaccine_name']),
            ('state', 'in', ['draft', 'administered']),
            ('next_due_date', '>=', today),
            ('id', '!=', vals.get('id', 0)),
        ])
        if existing:
            raise UserError(_('A vaccination for this patient and vaccine '
                              'already exists and is not due yet.'))

    def action_administer(self):
        for vaccination in self:
            if vaccination.state != 'draft':
                raise UserError(_('Only draft vaccinations can be '
                                  'administered.'))
        self.write({'state': 'administered'})
        for vaccination in self:
            if vaccination.next_due_date and vaccination.next_due_date < \
                    fields.Date.context_today(self):
                vaccination.state = 'overdue'

    def action_cancel(self):
        for vaccination in self:
            if vaccination.state not in ('draft', 'administered'):
                raise UserError(_('Only draft or administered vaccinations '
                                  'can be cancelled.'))
        self.state = 'cancelled'

    def action_purge_reminders(self):
        if not self.env.user.has_group(
                'sf_veterinary.group_sf_veterinary_manager'):
            raise UserError(_('Only a veterinary manager can purge '
                              'reminders.'))
        activities = self.env['mail.activity'].search([
            ('activity_type_id', '=', self.env.ref(
                'mail.mail_activity_data_todo').id),
            ('res_model', '=', 'sf.veterinary.vaccination'),
            ('done', '=', False),
        ])
        activities.action_done()

    def _cron_vaccination_reminders(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            vaccinations = self.with_company(company).search([
                ('state', 'in', ['administered', 'overdue']),
            ])
            for vaccination in vaccinations:
                if vaccination.next_due_date and vaccination.next_due_date \
                        < today:
                    vaccination.state = 'overdue'
            due = vaccinations.filtered(
                lambda v: v.next_due_date and v.next_due_date <= today +
                timedelta(days=company.sf_veterinary_reminder_days))
            for vaccination in due:
                if vaccination.activity_ids.filtered(
                        lambda a: a.activity_type_id == todo_type
                        and not a.done):
                    continue
                vaccination.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Vaccination reminder: %s - %s') % (
                        vaccination.name, vaccination.patient_id.name),
                    user_id=self.env.user.id)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.veterinary.appointment'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('next_due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.next_due_date
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.next_due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

