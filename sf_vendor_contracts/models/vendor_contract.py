# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class VendorContract(models.Model):
    _name = 'sf.vendor.contract'
    _description = 'Supplier Contract'
    _inherit = ['mail.thread']
    _order = 'date_end desc'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Supplier',
                                 required=True)
    contract_type = fields.Selection([
        ('supply', 'Supply'),
        ('service', 'Service'),
        ('maintenance', 'Maintenance'),
        ('framework', 'Framework'),
        ('other', 'Other'),
    ], string='Type', default='supply')
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date')
    amount_total = fields.Monetary(string='Total Amount', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.company.currency_id)
    renewal_days = fields.Integer(string='Renewal Notice (days)',
                                  default=60)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    clause_ids = fields.One2many('sf.vendor.contract.clause',
                                 'contract_id', string='Clauses')
    line_ids = fields.One2many('sf.vendor.contract.line',
                               'contract_id', string='Lines')
    version_ids = fields.One2many('sf.vendor.contract.version',
                                  'contract_id', string='Versions')
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Attachments')
    partner_ref = fields.Char(string='Supplier Reference')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for contract in self:
            if contract.date_end and \
                    contract.date_end < contract.date_start:
                raise UserError(
                    _('The end date cannot be before the start date.'))

    @api.constrains('amount_total')
    def _check_amount(self):
        for contract in self:
            if contract.amount_total < 0:
                raise UserError(
                    _('The contract amount cannot be negative.'))

    def action_activate(self):
        for contract in self:
            if contract.state != 'draft':
                raise UserError(
                    _('Only draft contracts can be activated.'))
            contract.state = 'active'
            contract._create_version('v1')

    def action_renew(self):
        view = self.env.ref(
            'sf_vendor_contracts.vendor_contract_renew_wizard_form')
        return {
            'name': _('Renew Contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.vendor.contract.renew.wizard',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'context': {'default_contract_id': self.id},
        }

    def action_cancel(self):
        view = self.env.ref(
            'sf_vendor_contracts.vendor_contract_cancel_wizard_form')
        return {
            'name': _('Cancel Contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.vendor.contract.cancel.wizard',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'context': {'default_contract_id': self.id},
        }

    def _create_version(self, version):
        self.ensure_one()
        if not version:
            raise UserError(
                _('A version number is required to renew a contract.'))
        self.env['sf.vendor.contract.version'].create({
            'contract_id': self.id,
            'version': version,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'amount_total': self.amount_total,
            'state': 'history',
        })

    def _cron_check_expiration(self):
        today = fields.Date.today()
        contracts = self.search([
            ('state', 'in', ('active', 'expiring')),
        ])
        for contract in contracts:
            if not contract.date_end:
                continue
            days_left = (contract.date_end - today).days
            if days_left < 0:
                contract.state = 'expired'
            elif days_left <= contract.renewal_days:
                if contract.state == 'active':
                    contract.state = 'expiring'
                    contract.activity_schedule(
                        'mail.mail_activity_data_todo',
                        _('Contract %s expires in %s days.') %
                        (contract.name, days_left),
                        user_id=contract.env.user.id)