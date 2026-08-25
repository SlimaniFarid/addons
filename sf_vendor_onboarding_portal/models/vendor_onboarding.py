# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class VendorOnboarding(models.Model):
    _name = 'sf.vendor.onboarding.portal.vendor.onboarding'
    _description = 'Vendor Onboarding'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(required=True, comodel_name='res.partner', ondelete='restrict')
    tax_id = fields.Char(string='Tax Id')
    bank_account = fields.Char(string='Bank Account')
    cert_documents = fields.Many2many('ir.attachment', string='Cert Documents')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)
    reviewer_id = fields.Many2one(comodel_name='res.users', ondelete='restrict')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.vendor.onboarding.portal.vendor.onboarding') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()
    
    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

