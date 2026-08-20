# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLibraryMember(models.Model):
    _name = 'sf.library.member'
    _description = 'Library Member'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='set null')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    registration_date = fields.Date(
        string='Registration date', default=fields.Date.context_today,
        tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    loan_ids = fields.One2many('sf.library.loan', 'member_id', string='Loans')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.library.member')
        return super().create(vals)

    def action_activate(self):
        for member in self:
            if member.status != 'draft':
                raise UserError(_('Only draft members can be activated.'))
        self.status = 'active'

    def action_block(self):
        if not self.env.user.has_group('sf_library.group_sf_library_manager'):
            raise UserError(_('Only a library manager can block members.'))
        for member in self:
            if member.status not in ('active', 'draft'):
                raise UserError(_('Only active or draft members can be blocked.'))
        self.status = 'blocked'
