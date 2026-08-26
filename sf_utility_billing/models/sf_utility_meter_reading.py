# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityMeterReading(models.Model):
    _name = 'sf.utility.meter.reading'
    _description = 'Utility Meter Reading'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.utility.activity.mixin']
    _order = 'reading_date asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    meter_id = fields.Many2one('sf.utility.meter', string='Meter', required=True, ondelete='cascade')
    campaign_id = fields.Many2one('sf.utility.campaign', string='Campaign', required=True, ondelete='cascade')
    reading_date = fields.Date(string='Reading Date', required=True, default=fields.Date.context_today)
    index = fields.Float(string='Index', required=True)
    consumption = fields.Float(string='Consumption', compute='_compute_consumption', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends(
        'meter_id.opening_index',
        'meter_id.reading_ids.state',
        'meter_id.reading_ids.index',
        'meter_id.reading_ids.reading_date',
        'index',
        'reading_date',
    )
    def _compute_consumption(self):
        for reading in self:
            if reading.index is not None and reading.meter_id:
                previous = reading.meter_id.reading_ids.filtered(
                    lambda r: r.state == 'validated'
                    and r.id != reading.id
                    and (r.reading_date, r.id) < (reading.reading_date, reading.id)
                ).sorted(key=lambda r: (r.reading_date, r.id))
                base = previous[-1].index if previous else reading.meter_id.opening_index or 0.0
                reading.consumption = reading.index - base
            else:
                reading.consumption = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.utility.meter.reading')
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if record.state == 'validated':
                if set(vals) - {'state'}:
                    raise UserError(_('A validated reading cannot be modified.'))
                if vals.get('state', record.state) not in ('rejected',):
                    raise UserError(_('A validated reading cannot be modified.'))
        if any(record.state == 'validated'
               and vals.get('state', record.state) == 'rejected' for record in self):
            self._check_manager()
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_utility_billing.group_sf_utility_manager'):
            raise UserError(_('Only a utility manager can perform this action.'))

    def action_done(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft readings can be marked done.'))
        self.state = 'done'

    def action_validate(self):
        self.ensure_one()
        if self.state not in ('done', 'draft'):
            raise UserError(_('Only done readings can be validated.'))
        if self.consumption < 0:
            self.state = 'rejected'
            raise UserError(_('The index is lower than the previous validated reading; the reading has been rejected.'))
        self.state = 'validated'
        self.meter_id._sf_check_anomaly(self)

    def action_reject(self):
        self.ensure_one()
        if self.state == 'validated':
            self._check_manager()
        if self.state not in ('done', 'validated'):
            raise UserError(_('Only done or validated readings can be rejected.'))
        self.state = 'rejected'

    def action_reset(self):
        self.ensure_one()
        if self.state != 'rejected':
            raise UserError(_('Only rejected readings can be reset.'))
        self.state = 'draft'