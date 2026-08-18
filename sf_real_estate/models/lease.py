# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Lease(models.Model):
    _name = 'sf.realestate.lease'
    _description = 'Lease'
    _rec_name = 'name'
    _order = 'date_start desc'

    name = fields.Char(string='Number', required=True, readonly=True,
                       default=lambda self: _('New'))
    property_id = fields.Many2one(
        'sf.realestate.property', string='Property', required=True,
        ondelete='cascade')
    tenant_id = fields.Many2one(
        'res.partner', string='Tenant', required=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date')
    rent = fields.Monetary(string='Monthly Rent', required=True)
    deposit = fields.Monetary(string='Deposit')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    invoice_ids = fields.One2many('sf.realestate.rent.invoice',
                                  'lease_id', string='Invoices')
    total_invoiced = fields.Monetary(
        string='Total Invoiced', compute='_compute_totals')
    total_paid = fields.Monetary(
        string='Total Paid', compute='_compute_totals')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('sf.realestate.lease')
            vals['name'] = seq or '/'
        return super().create(vals)

    @api.depends('invoice_ids', 'invoice_ids.amount_total',
                 'invoice_ids.payment_state')
    def _compute_totals(self):
        for lease in self:
            lease.total_invoiced = sum(
                lease.invoice_ids.mapped('amount_total') or [0.0])
            lease.total_paid = sum(
                i.amount_total for i in lease.invoice_ids
                if i.payment_state == 'paid')

    def action_activate(self):
        self.write({'state': 'active'})
        self.property_id.write({'state': 'rented'})

    def action_close(self):
        self.write({'state': 'closed'})
        self.property_id.write({'state': 'available'})

    def action_generate_invoices(self, periods=1):
        """Generate rent invoices for the lease."""
        self.ensure_one()
        for period in range(periods):
            self.env['sf.realestate.rent.invoice'].create({
                'lease_id': self.id,
                'tenant_id': self.tenant_id.id,
                'property_id': self.property_id.id,
                'period_label': 'Month %s' % (period + 1),
                'amount': self.rent,
            })
        return True