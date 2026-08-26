# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDonationReceipt(models.Model):
    _name = 'sf.donation.receipt'
    _description = 'Donation Receipt'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='set null')
    donor = fields.Char(string='Donor')
    amount = fields.Float(string='Amount', required=True)
    receipt_date = fields.Date(
        string='Receipt date', default=fields.Date.context_today)
    fiscal_ref = fields.Char(string='Fiscal reference')
    payment_id = fields.Many2one(
        'sf.donation.payment', string='Payment', ondelete='set null',
        index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.donation.receipt')
        if vals.get('payment_id'):
            payment = self.env['sf.donation.payment'].browse(
                vals['payment_id'])
            if not vals.get('amount'):
                vals['amount'] = payment.amount
            if not vals.get('donor'):
                vals['donor'] = payment.donor
        return super().create(vals)

    def action_issue(self):
        if not self.env.user.has_group('sf_donations.group_sf_donation_manager'):
            raise UserError(_('Only a donation manager can issue receipts.'))
        for receipt in self:
            if receipt.state != 'draft':
                raise UserError(_('Only draft receipts can be issued.'))
        self.state = 'issued'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.donation.campaign'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

