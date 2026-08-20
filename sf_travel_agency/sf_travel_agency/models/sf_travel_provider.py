# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfTravelProvider(models.Model):
    _name = 'sf.travel.provider'
    _description = 'Travel Provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, readonly=True, copy=False)
    provider_type = fields.Selection([
        ('hotel', 'Hotel'),
        ('transport', 'Transport'),
        ('activity', 'Activity'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ], string='Provider Type', required=True, default='other')
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict')
    contact_name = fields.Char(string='Contact Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    contract_ref = fields.Char(string='Contract Reference')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.travel.provider') or 'New'
        return super(SfTravelProvider, self).create(vals)

    def write(self, vals):
        if 'active' in vals and not self.env.user.has_group('sf_travel_agency.group_sf_travel_agency_manager'):
            raise UserError(_('Only managers can archive providers.'))
        return super(SfTravelProvider, self).write(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_archive(self):
        self.write({'active': False, 'state': 'archived'})
