from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class SpaBooking(models.Model):
    _name = 'sf.spa.booking'
    _description = 'Spa Booking'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'start_datetime desc'
    _sequence_code = 'sf.spa.booking'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    service_id = fields.Many2one('sf.spa.service', string='Service', required=True, tracking=True)
    resource_id = fields.Many2one('sf.spa.resource', string='Resource', tracking=True)
    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', tracking=True)
    start_datetime = fields.Datetime(string='Start', required=True, tracking=True)
    end_datetime = fields.Datetime(string='End', compute='_compute_end_datetime', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], string='State', default='draft', tracking=True)
    package_id = fields.Many2one('sf.spa.package', string='Package')
    cure_id = fields.Many2one('sf.spa.cure.instance', string='Cure')
    notes = fields.Text(string='Notes')
    client_preferences = fields.Text(string='Client Preferences')
    treatment_notes = fields.Text(string='Treatment Notes')
    recommended_product_ids = fields.Many2many('product.product', string='Recommended Products')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.depends('start_datetime', 'service_id.duration_minutes')
    def _compute_end_datetime(self):
        for record in self:
            if record.start_datetime and record.service_id:
                record.end_datetime = record.start_datetime + timedelta(minutes=record.service_id.duration_minutes)
            else:
                record.end_datetime = record.start_datetime

    @api.constrains('resource_id', 'start_datetime', 'end_datetime', 'state')
    def _check_resource_conflict(self):
        for record in self:
            if record.state in ('draft', 'cancelled', 'no_show') or not record.resource_id or not record.start_datetime:
                continue
            conflicting = self.search([
                ('resource_id', '=', record.resource_id.id),
                ('state', 'in', ['confirmed', 'in_progress']),
                ('id', '!=', record.id),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
            ])
            if conflicting:
                raise ValidationError(_('Resource %s is already booked for this time slot.') % record.resource_id.name)

    @api.constrains('therapist_id', 'start_datetime', 'end_datetime', 'state')
    def _check_therapist_conflict(self):
        for record in self:
            if record.state in ('draft', 'cancelled', 'no_show') or not record.therapist_id or not record.start_datetime:
                continue
            conflicting = self.search([
                ('therapist_id', '=', record.therapist_id.id),
                ('state', 'in', ['confirmed', 'in_progress']),
                ('id', '!=', record.id),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
            ])
            if conflicting:
                raise ValidationError(_('Therapist %s is already booked for this time slot.') % record.therapist_id.name)

    @api.constrains('therapist_id', 'service_id')
    def _check_therapist_skills(self):
        for record in self:
            if record.therapist_id and record.service_id and record.service_id.therapist_skill_ids:
                missing_skills = record.service_id.therapist_skill_ids - record.therapist_id.skill_ids
                if missing_skills:
                    raise ValidationError(_('Therapist %s lacks required skills: %s') % (
                        record.therapist_id.name, ', '.join(missing_skills.mapped('name'))))

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                continue
            record.state = 'confirmed'

    def action_start(self):
        for record in self:
            if record.state != 'confirmed':
                continue
            record.state = 'in_progress'

    def action_done(self):
        for record in self:
            if record.state != 'in_progress':
                continue
            record.state = 'done'
            if record.package_id:
                record.package_id._consume_session()

    def action_cancel(self):
        for record in self:
            if record.state in ('done', 'cancelled'):
                continue
            record.state = 'cancelled'

    def action_no_show(self):
        for record in self:
            if record.state != 'confirmed':
                continue
            record.state = 'no_show'

    def action_draft(self):
        for record in self:
            if record.state not in ('cancelled', 'no_show'):
                continue
            record.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('service_id') and not vals.get('resource_id'):
                service = self.env['sf.spa.service'].browse(vals['service_id'])
                if service.resource_type_required:
                    vals['resource_id'] = service.resource_type_required.id
        return super().create(vals_list)