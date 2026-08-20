# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityCampaign(models.Model):
    _name = 'sf.utility.campaign'
    _description = 'Utility Reading Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.utility.activity.mixin']
    _order = 'period_start desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    period_start = fields.Date(string='Period Start', required=True)
    period_end = fields.Date(string='Period End', required=True)
    meter_ids = fields.Many2many('sf.utility.meter', string='Meters')
    reading_ids = fields.One2many('sf.utility.meter.reading', 'campaign_id', string='Readings')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.constrains('period_start', 'period_end')
    def _check_period(self):
        for campaign in self:
            if campaign.period_start and campaign.period_end \
                    and campaign.period_end < campaign.period_start:
                raise UserError(_('The period end must be on or after the period start.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.utility.campaign')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_utility_billing.group_sf_utility_manager'):
            raise UserError(_('Only a utility manager can perform this action.'))

    def _prepare_readings(self):
        self.ensure_one()
        readings = self.env['sf.utility.meter.reading']
        for meter in self.meter_ids.filtered(lambda m: m.active):
            existing = self.reading_ids.filtered(lambda r: r.meter_id.id == meter.id)
            if existing:
                continue
            readings |= self.env['sf.utility.meter.reading'].create({
                'meter_id': meter.id,
                'campaign_id': self.id,
                'reading_date': self.period_end or fields.Date.context_today(self),
                'index': meter.last_index,
                'state': 'draft',
                'company_id': meter.company_id.id,
            })
        return readings

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft campaigns can be opened.'))
        self._prepare_readings()
        self.state = 'open'

    def action_close(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open campaigns can be closed.'))
        unvalidated = self.reading_ids.filtered(lambda r: r.state not in ('validated', 'rejected'))
        if unvalidated:
            raise UserError(_('All readings must be validated or rejected before closing the campaign.'))
        for reading in self.reading_ids.filtered(lambda r: r.state == 'validated'):
            if reading.consumption > 0:
                existing = self.env['sf.utility.invoice'].search([
                    ('reading_id', '=', reading.id),
                    ('campaign_id', '=', self.id),
                ])
                if not existing:
                    self.env['sf.utility.invoice'].create({
                        'meter_id': reading.meter_id.id,
                        'campaign_id': self.id,
                        'reading_id': reading.id,
                        'consumption': reading.consumption,
                        'company_id': reading.meter_id.company_id.id,
                    })
        self.state = 'closed'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state not in ('draft', 'open'):
            raise UserError(_('Only draft or open campaigns can be cancelled.'))
        self.state = 'cancelled'