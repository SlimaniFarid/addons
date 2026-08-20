# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class VisitorVisit(models.Model):
    _name = 'sf.visitor.visit'
    _description = 'Visitor Visit'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    person_id = fields.Many2one('sf.visitor.person', string='Visitor',
                                ondelete='restrict')
    full_name = fields.Char(string='Full name')
    visiting_company_id = fields.Many2one('res.partner',
                                          string='Visiting company',
                                          ondelete='restrict')
    visit_type = fields.Selection([
        ('client', 'Client'),
        ('supplier', 'Supplier'),
        ('visitor', 'Visitor'),
        ('courier', 'Courier'),
        ('candidate', 'Candidate'),
        ('other', 'Other'),
    ], string='Type', required=True)
    gate_id = fields.Many2one('sf.visitor.gate', string='Gate / Site',
                              required=True, ondelete='restrict', index=True)
    host_id = fields.Many2one('hr.employee', string='Host / Person met',
                              ondelete='restrict')
    purpose = fields.Text(string='Purpose')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('no_show', 'No Show'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    planned_date = fields.Datetime(string='Planned visit')
    check_in = fields.Datetime(string='Check-in', index=True)
    check_out = fields.Datetime(string='Check-out')
    badge_number = fields.Char(string='Badge number', index=True)
    zone = fields.Char(string='Authorized zone')
    authorized_duration_hours = fields.Float(
        string='Authorized duration (hours)', default=8.0)
    safety_rule_ok = fields.Boolean(string='Safety rules accepted')
    rule_version = fields.Integer(string='Rule version accepted')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('badge_uniq', 'UNIQUE(badge_number)',
         _('This badge number is already in use.')),
    ]

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        for visit in self:
            if visit.check_in and visit.check_out and \
                    visit.check_out < visit.check_in:
                raise ValidationError(_('Check-out cannot be before '
                                        'check-in.'))

    @api.constrains('visit_type', 'host_id')
    def _check_host_required(self):
        for visit in self:
            if visit.visit_type in ('client', 'supplier') and \
                    not visit.host_id:
                raise ValidationError(_('A host is required for client and '
                                        'supplier visits.'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.visitor.visit')
            vals['name'] = 'VIS-%s' % seq
        return super().create(vals)

    def action_check_in(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft visits can be checked in.'))
        has_rules = bool(self.gate_id.rule_ids.filtered(lambda r: r.active))
        if has_rules and not self.safety_rule_ok:
            raise UserError(_('The visitor must accept the site safety '
                              'rules before checking in.'))
        badge_seq = self.env['ir.sequence'].next_by_code('sf.visitor.badge')
        version = max(self.gate_id.rule_ids.filtered(
            lambda r: r.active).mapped('version') or [0])
        self.write({
            'badge_number': 'B-%s' % badge_seq,
            'check_in': fields.Datetime.now(),
            'state': 'checked_in',
            'rule_version': version,
        })
        if self.host_id:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_('Visitor %s has arrived')
                % (self.person_id.name or self.full_name),
                user_id=self.host_id.user_id.id
                if self.host_id.user_id else self.env.user.id)

    def action_checkin_wizard(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft visits can be checked in.'))
        return {
            'name': _('Check In Visitor'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.visitor.checkin.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_visit_id': self.id,
                        'default_gate_id': self.gate_id.id,
                        'default_zone': self.zone,
                        'default_authorized_duration_hours':
                            self.authorized_duration_hours,
                        'default_safety_rule_ok': self.safety_rule_ok},
        }

    def action_check_out(self):
        self.ensure_one()
        if self.state != 'checked_in':
            raise UserError(_('Only checked-in visits can be checked out.'))
        self.write({
            'check_out': fields.Datetime.now(),
            'state': 'checked_out',
        })

    def action_no_show(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft visits can be marked as no show.'))
        self.state = 'no_show'

    def action_archive(self):
        self.ensure_one()
        if self.state != 'checked_out':
            raise UserError(_('Only checked-out visits can be archived.'))
        self.state = 'archived'
        self.active = False

    def unlink(self):
        for visit in self:
            if visit.state == 'checked_in':
                raise UserError(_('A checked-in visitor cannot be deleted. '
                                  'Check the visitor out first.'))
        return super().unlink()

    def _check_visitor_overtime(self):
        now = fields.Datetime.now()
        visits = self.search([('state', '=', 'checked_in')])
        for visit in visits:
            if not visit.check_in:
                continue
            allowed_until = visit.check_in + timedelta(
                hours=visit.authorized_duration_hours
                + visit.company_id.sf_visitor_alert_hours)
            if now > allowed_until:
                manager = visit.gate_id.manager_id
                user = manager.user_id if manager and manager.user_id \
                    else self.env.user
                visit.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Visitor overtime on site: %s')
                    % (visit.person_id.name or visit.full_name),
                    user_id=user.id)
        planned = self.search([('state', '=', 'draft'),
                               ('planned_date', '!=', False)])
        for visit in planned:
            if visit.planned_date < now:
                visit.state = 'no_show'


class VisitorGate(models.Model):
    _name = 'sf.visitor.gate'
    _description = 'Visitor Gate / Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    site_code = fields.Char(string='Site code')
    address = fields.Char(string='Address')
    manager_id = fields.Many2one('hr.employee', string='Site manager',
                                 ondelete='restrict')
    rule_ids = fields.One2many('sf.visitor.rule', 'gate_id',
                               string='Safety rules')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This site already exists.')),
    ]


class VisitorRule(models.Model):
    _name = 'sf.visitor.rule'
    _description = 'Visitor Safety Rule'
    _order = 'gate_id, version'

    gate_id = fields.Many2one('sf.visitor.gate', string='Gate / Site',
                              required=True, ondelete='cascade')
    version = fields.Integer(string='Version', default=1, required=True)
    name = fields.Char(string='Name', required=True)
    body = fields.Html(string='Rules content')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='gate_id.company_id', store=True,
                                 readonly=True)

    _sql_constraints = [
        ('gate_version_uniq', 'UNIQUE(gate_id, version)',
         _('This rule version already exists for this site.')),
    ]


class VisitorPerson(models.Model):
    _name = 'sf.visitor.person'
    _description = 'Known Visitor Person'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    visiting_company_id = fields.Many2one('res.partner', string='Company',
                                          ondelete='restrict')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    known = fields.Boolean(string='Known visitor', default=True)
    visit_ids = fields.One2many('sf.visitor.visit', 'person_id',
                                string='Visits')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_company_uniq', 'UNIQUE(name, visiting_company_id)',
         _('This visitor already exists for this company.')),
    ]


class VisitorCheckinWizard(models.TransientModel):
    _name = 'sf.visitor.checkin.wizard'
    _description = 'Visitor Check-in'

    visit_id = fields.Many2one('sf.visitor.visit', string='Visit',
                               required=True)
    gate_id = fields.Many2one('sf.visitor.gate', string='Gate / Site',
                              required=True)
    zone = fields.Char(string='Authorized zone')
    authorized_duration_hours = fields.Float(
        string='Authorized duration (hours)', default=8.0)
    safety_rule_ok = fields.Boolean(string='I accept the site safety rules')

    def action_check_in(self):
        self.ensure_one()
        visit = self.visit_id
        visit.write({
            'gate_id': self.gate_id.id,
            'zone': self.zone,
            'authorized_duration_hours': self.authorized_duration_hours,
            'safety_rule_ok': self.safety_rule_ok,
        })
        visit.action_check_in()
        return {'type': 'ir.actions.act_window_close'}