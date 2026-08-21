# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfFreightRule(models.Model):
    _name = 'sf.freight.rule'
    _description = 'Freight Audit Verification Rule'
    _order = 'sequence, id'

    name = fields.Char(string='Rule Name', required=True)
    sequence = fields.Integer(default=10)
    rule_type = fields.Selection([
        ('rate', 'Rate Variance'),
        ('surcharge', 'Unauthorized Surcharge'),
        ('weight_dim', 'Weight / Dimension Mismatch'),
        ('duplicate', 'Duplicate Billing'),
        ('phantom', 'Phantom Shipment'),
        ('vat', 'VAT Error'),
    ], string='Rule Type', required=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity when triggered', default='medium')
    action = fields.Selection([
        ('flag', 'Flag Finding'),
        ('block', 'Block Payment'),
    ], string='Action', default='flag')
    condition_domain = fields.Text(
        string='Extra Condition (domain)',
        help='Optional domain on sf.freight.invoice.line to restrict '
             'when this rule applies. Empty = always.')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True, copy=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    def write(self, vals):
        if 'state' in vals:
            flow = {'draft': {'draft', 'active'},
                    'active': {'active', 'archived'},
                    'archived': {'archived'}}
            for rec in self:
                if vals['state'] not in flow.get(rec.state, set()):
                    raise UserError(_(
                        'Invalid rule transition %s -> %s.')
                        % (rec.state, vals['state']))
        return super().write(vals)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_archive(self):
        self.write({'state': 'archived'})
