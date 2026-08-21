# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfFranchiseContract(models.Model):
    _name = 'sf.franchise.contract'
    _description = 'Franchise Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.franchise.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Franchisee', required=True,
                                 ondelete='restrict')
    territory = fields.Char(string='Territory')
    royalty_type = fields.Selection([
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage of Sales'),
    ], string='Royalty Type', default='percentage', required=True)
    fixed_amount = fields.Monetary(string='Fixed Royalty', currency_field='currency_id')
    royalty_percent = fields.Float(string='Royalty Percentage (%)', default=0.0)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ], string='Status', default='draft', copy=False)
    declaration_ids = fields.One2many('sf.franchise.declaration', 'contract_id',
                                      string='Sales Declarations')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('royalty_percent_range', 'CHECK (royalty_percent >= 0 AND royalty_percent <= 100)',
         'The royalty percentage must be between 0 and 100.'),
        ('fixed_amount_non_negative', 'CHECK (fixed_amount >= 0)',
         'The fixed royalty amount cannot be negative.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.franchise.contract')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_franchise.group_sf_franchise_manager'):
            raise UserError(_('Only a franchise manager can perform this action.'))

    def action_activate(self):
        self._check_manager()
        for contract in self:
            if contract.state != 'draft':
                raise UserError(_('Only draft contracts can be activated.'))
            contract.state = 'active'
            contract.message_post(body=_('The franchise contract was activated.'))

    def action_suspend(self):
        self._check_manager()
        for contract in self:
            if contract.state != 'active':
                raise UserError(_('Only active contracts can be suspended.'))
            contract.state = 'suspended'
            contract.message_post(body=_('The franchise contract was suspended.'))

    def action_terminate(self):
        self._check_manager()
        for contract in self:
            if contract.state not in ('active', 'suspended'):
                raise UserError(_('Only active or suspended contracts can be terminated.'))
            contract.state = 'terminated'
            contract.message_post(body=_('The franchise contract was terminated.'))