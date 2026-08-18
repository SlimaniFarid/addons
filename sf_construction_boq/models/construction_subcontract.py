from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ConstructionSubcontract(models.Model):
    _name = 'construction.subcontract'
    _description = 'Subcontract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    project_id = fields.Many2one('project.project', string='Project', ondelete='restrict', required=True, tracking=True)
    contractor_id = fields.Many2one('res.partner', string='Contractor', ondelete='restrict', required=True, tracking=True)
    contract_amount = fields.Monetary(string='Contract Amount', currency_field='currency_id', tracking=True)
    retention_rate = fields.Float(string='Retention Rate (%)', default=10.0, tracking=True)
    advance_amount = fields.Monetary(string='Advance', currency_field='currency_id', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    certificate_ids = fields.One2many('construction.payment.certificate', 'subcontract_id', string='Payment Certificates')
    amount_certified = fields.Monetary(string='Certified', currency_field='currency_id',
                                       compute='_compute_amount_certified', store=True)

    @api.depends('certificate_ids.amount_to_pay')
    def _compute_amount_certified(self):
        for sub in self:
            sub.amount_certified = sum(sub.certificate_ids.mapped('amount_to_pay'))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.subcontract') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for sub in self:
            if sub.state != 'draft':
                raise UserError(_('Only a draft subcontract can be confirmed.'))
            sub.state = 'confirmed'

    def action_start(self):
        for sub in self:
            if sub.state != 'confirmed':
                raise UserError(_('Only a confirmed subcontract can be started.'))
            sub.state = 'in_progress'

    def action_close(self):
        for sub in self:
            sub.state = 'closed'

    def action_cancel(self):
        for sub in self:
            if sub.state in ('closed',):
                raise UserError(_('A closed subcontract cannot be cancelled.'))
            sub.state = 'cancelled'

    def action_create_certificate(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'in_progress'):
            raise UserError(_('The subcontract must be confirmed or in progress to create a payment certificate.'))
        certificate = self.env['construction.payment.certificate'].create({
            'subcontract_id': self.id,
            'project_id': self.project_id.id,
            'contractor_id': self.contractor_id.id,
            'retention_rate': self.retention_rate,
        })
        return {
            'name': _('Payment Certificate'),
            'type': 'ir.actions.act_window',
            'res_model': 'construction.payment.certificate',
            'view_mode': 'form',
            'res_id': certificate.id,
            'target': 'current',
        }
