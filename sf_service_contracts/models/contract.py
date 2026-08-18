# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ServiceContract(models.Model):
    _name = 'sf.service.contract'
    _description = 'Service Contract'
    _rec_name = 'name'
    _order = 'date_start desc'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True)
    sla_tier_id = fields.Many2one('sf.sla.tier', string='SLA Tier')
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date')
    recurring_amount = fields.Monetary(string='Recurring Amount')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    sla_event_ids = fields.One2many('sf.sla.event', 'contract_id',
                                    string='SLA Events')
    breached_events = fields.Integer(string='Breached SLAs',
                                     compute='_compute_breached')

    @api.depends('sla_event_ids.breached')
    def _compute_breached(self):
        for contract in self:
            contract.breached_events = len(
                contract.sla_event_ids.filtered(lambda e: e.breached))

    def action_activate(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_check_expiry(self):
        today = fields.Date.today()
        for contract in self:
            if (contract.state == 'active' and contract.date_end and
                    contract.date_end < today):
                contract.state = 'expired'
        return True