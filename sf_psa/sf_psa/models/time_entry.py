# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PsaTimeEntry(models.Model):
    _name = 'sf.psa.time.entry'
    _description = 'PSA Time Entry'
    _order = 'date desc'

    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    engagement_id = fields.Many2one('sf.psa.engagement', string='Engagement',
                                    required=True)
    assignment_id = fields.Many2one('sf.psa.assignment', string='Assignment',
                                    ondelete='cascade')
    resource_id = fields.Many2one('sf.psa.resource', string='Resource',
                                  required=True)
    hours = fields.Float(string='Hours', required=True, default=1.0)
    description = fields.Text(string='Description')
    billable = fields.Boolean(string='Billable', default=True)
    amount = fields.Float(string='Amount', compute='_compute_amount',
                          store=True)

    @api.depends('hours', 'resource_id.hourly_rate', 'billable')
    def _compute_amount(self):
        for entry in self:
            rate = entry.resource_id.hourly_rate or 0.0
            entry.amount = (entry.hours * rate) if entry.billable else 0.0