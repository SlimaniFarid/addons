# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class RentInvoice(models.Model):
    _name = 'sf.realestate.rent.invoice'
    _description = 'Rent Invoice'
    _rec_name = 'name'
    _order = 'date desc'

    name = fields.Char(string='Number', required=True, readonly=True,
                       default=lambda self: _('New'))
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    lease_id = fields.Many2one(
        'sf.realestate.lease', string='Lease', required=True,
        ondelete='cascade')
    tenant_id = fields.Many2one('res.partner', string='Tenant', required=True)
    property_id = fields.Many2one(
        'sf.realestate.property', string='Property', required=True)
    period_label = fields.Char(string='Period')
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.realestate.rent.invoice')
            vals['name'] = seq or '/'
        return super().create(vals)

    def action_post(self):
        self.write({'state': 'posted'})

    def action_paid(self):
        self.write({'state': 'paid'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.realestate.lease'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
