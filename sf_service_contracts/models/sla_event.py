# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SlaEvent(models.Model):
    _name = 'sf.sla.event'
    _description = 'SLA Event'
    _rec_name = 'reference'
    _order = 'create_date desc'

    contract_id = fields.Many2one('sf.service.contract', string='Contract',
                                  required=True, ondelete='cascade')
    reference = fields.Char(string='Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 related='contract_id.partner_id',
                                 store=True, readonly=True)
    date_opened = fields.Datetime(string='Opened', required=True)
    date_responded = fields.Datetime(string='Responded')
    date_resolved = fields.Datetime(string='Resolved')
    response_hours = fields.Integer(string='Response Target (h)',
                                    compute='_compute_targets')
    resolution_hours = fields.Integer(string='Resolution Target (h)',
                                      compute='_compute_targets')
    response_breached = fields.Boolean(string='Response Breached',
                                       compute='_compute_breaches',
                                       store=True)
    resolution_breached = fields.Boolean(string='Resolution Breached',
                                         compute='_compute_breaches',
                                         store=True)
    breached = fields.Boolean(string='Breached',
                              compute='_compute_breaches', store=True)

    @api.depends('contract_id.sla_tier_id')
    def _compute_targets(self):
        for event in self:
            tier = event.contract_id.sla_tier_id
            event.response_hours = tier.response_hours if tier else 0
            event.resolution_hours = tier.resolution_hours if tier else 0

    @api.depends('date_opened', 'date_responded', 'date_resolved',
                 'response_hours', 'resolution_hours')
    def _compute_breaches(self):
        for event in self:
            resp = False
            resol = False
            if event.date_opened:
                if event.date_responded:
                    resp = ((event.date_responded - event.date_opened)
                            .total_seconds() / 3600.0 > event.response_hours)
                if event.date_resolved:
                    resol = ((event.date_resolved - event.date_opened)
                             .total_seconds() / 3600.0 >
                             event.resolution_hours)
            event.response_breached = resp
            event.resolution_breached = resol
            event.breached = resp or resol