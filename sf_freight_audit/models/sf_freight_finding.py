# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfFreightFinding(models.Model):
    _name = 'sf.freight.finding'
    _description = 'Freight Audit Finding'
    _order = 'severity desc, id desc'

    invoice_id = fields.Many2one('sf.freight.invoice', string='Invoice',
                                 required=True, ondelete='cascade',
                                 index=True)
    invoice_line_id = fields.Many2one('sf.freight.invoice.line',
                                      string='Invoice Line',
                                      ondelete='cascade')
    rule_id = fields.Many2one('sf.freight.rule', string='Rule',
                              ondelete='set null')
    finding_type = fields.Selection([
        ('rate_variance', 'Rate Variance'),
        ('surcharge_unauthorized', 'Unauthorized Surcharge'),
        ('weight_dim_mismatch', 'Weight / Dimension Mismatch'),
        ('duplicate_billing', 'Duplicate Billing'),
        ('phantom_shipment', 'Phantom Shipment'),
        ('vat_error', 'VAT Error'),
    ], string='Type', required=True, index=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', default='medium', index=True)
    expected_amount = fields.Monetary(string='Expected Amount',
                                      currency_field='currency_id')
    actual_amount = fields.Monetary(string='Billed Amount',
                                    currency_field='currency_id')
    variance_amount = fields.Monetary(
        string='Variance Amount', currency_field='currency_id',
        compute='_compute_variance_amount', store=True)
    currency_id = fields.Many2one(related='invoice_id.currency_id')
    status = fields.Selection([
        ('open', 'Open'),
        ('explained', 'Explained'),
        ('disputed', 'Disputed'),
        ('resolved', 'Resolved'),
        ('waived', 'Waived'),
    ], string='Status', default='open', tracking=True, index=True)
    dispute_id = fields.Many2one('sf.freight.dispute', string='Dispute',
                                 ondelete='set null')
    note = fields.Html(string='Note')

    @api.depends('expected_amount', 'actual_amount')
    def _compute_variance_amount(self):
        for f in self:
            f.variance_amount = f.actual_amount - f.expected_amount

    def write(self, vals):
        if 'status' in vals:
            for rec in self:
                if rec.status == 'resolved' and vals['status'] != 'resolved':
                    raise UserError(_(
                        'A resolved finding cannot be reopened.'))
        return super().write(vals)

    def action_waive(self):
        self.write({'status': 'waived'})

    def action_mark_explained(self):
        self.write({'status': 'explained'})
