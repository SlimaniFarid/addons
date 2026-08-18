from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ConstructionPaymentCertificate(models.Model):
    _name = 'construction.payment.certificate'
    _description = 'Payment Certificate (IPC)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    project_id = fields.Many2one('project.project', string='Project', ondelete='restrict', required=True, tracking=True)
    contractor_id = fields.Many2one('res.partner', string='Contractor', ondelete='restrict', required=True, tracking=True)
    subcontract_id = fields.Many2one('construction.subcontract', string='Subcontract', ondelete='restrict', tracking=True)
    period_start = fields.Date(string='Period Start', required=True, tracking=True)
    period_end = fields.Date(string='Period End', required=True, tracking=True)
    date = fields.Date(string='Certificate Date', default=fields.Date.context_today, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    retention_rate = fields.Float(string='Retention Rate (%)', default=10.0, tracking=True)
    certificate_line_ids = fields.One2many('construction.payment.certificate.line', 'certificate_id', string='Lines')
    previous_certified = fields.Monetary(string='Previously Certified', currency_field='currency_id',
                                         compute='_compute_amounts', readonly=True)
    current_amount = fields.Monetary(string='Current Period', currency_field='currency_id',
                                     compute='_compute_amounts', store=True)
    retention_amount = fields.Monetary(string='Retention', currency_field='currency_id',
                                       compute='_compute_amounts', store=True)
    net_amount = fields.Monetary(string='Net Amount', currency_field='currency_id',
                                 compute='_compute_amounts', store=True)
    amount_to_pay = fields.Monetary(string='Amount to Pay', currency_field='currency_id',
                                    compute='_compute_amounts', store=True)

    @api.constrains('period_start', 'period_end')
    def _check_period(self):
        for cert in self:
            if cert.period_start and cert.period_end and cert.period_start > cert.period_end:
                raise UserError(_('The period start date cannot be after the period end date.'))

    @api.depends('certificate_line_ids.current_amount', 'retention_rate', 'subcontract_id')
    def _compute_amounts(self):
        for cert in self:
            current = sum(cert.certificate_line_ids.mapped('current_amount'))
            previous = 0.0
            if cert.subcontract_id:
                previous = sum(cert.subcontract_id.certificate_ids.filtered(
                    lambda c: c.id != cert.id and c.state in ('confirmed', 'paid')).mapped('net_amount'))
            retention = current * cert.retention_rate / 100.0
            net = current - retention
            cert.previous_certified = previous
            cert.current_amount = current
            cert.retention_amount = retention
            cert.net_amount = net
            cert.amount_to_pay = net

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.payment.certificate') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for cert in self:
            if not cert.certificate_line_ids:
                raise UserError(_('Cannot confirm a certificate without lines.'))
            cert.state = 'confirmed'

    def action_paid(self):
        for cert in self:
            if cert.state != 'confirmed':
                raise UserError(_('Only a confirmed certificate can be marked as paid.'))
            cert.state = 'paid'

    def action_cancel(self):
        for cert in self:
            if cert.state in ('paid',):
                raise UserError(_('A paid certificate cannot be cancelled.'))
            cert.state = 'cancelled'


class ConstructionPaymentCertificateLine(models.Model):
    _name = 'construction.payment.certificate.line'
    _description = 'Payment Certificate Line'
    _order = 'certificate_id, sequence, id'

    certificate_id = fields.Many2one('construction.payment.certificate', string='Certificate',
                                     ondelete='cascade', required=True, index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    boq_line_id = fields.Many2one('construction.boq.line', string='BOQ Line', ondelete='set null')
    description = fields.Text(string='Description', required=True)
    previous_quantity = fields.Float(string='Previous Qty', default=0.0)
    current_quantity = fields.Float(string='Current Qty', default=0.0)
    total_quantity = fields.Float(string='Total Qty', compute='_compute_quantity', store=True)
    unit_price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    current_amount = fields.Monetary(string='Amount', currency_field='currency_id',
                                     compute='_compute_amount', store=True)
    currency_id = fields.Many2one('res.currency', related='certificate_id.currency_id', readonly=True)

    @api.depends('previous_quantity', 'current_quantity')
    def _compute_quantity(self):
        for line in self:
            line.total_quantity = line.previous_quantity + line.current_quantity

    @api.depends('current_quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.current_amount = line.current_quantity * line.unit_price
