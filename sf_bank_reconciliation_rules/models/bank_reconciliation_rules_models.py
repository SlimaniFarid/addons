# -*- coding: utf-8 -*-
"""Bank Reconciliation Rule Builder models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBrecRule(models.Model):
    _name = 'sf.brec.rule'
    _description = 'Reconciliation Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    name = fields.Char(string='Rule Name', required=True)
    match_label = fields.Char(string='Label Contains')
    amount_min = fields.Float(string='Amount Min')
    amount_max = fields.Float(string='Amount Max')
    priority = fields.Integer(string='Priority', default=10)
    partner_id = fields.Many2one('res.partner', string='Suggested Partner')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.brec.rule') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_archived(self):
        self.write({'state': 'archived'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.brec.rule'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.brec.rule'

    def action_refresh_business(self):
        """Pull open / overdue amounts for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            moves = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', partner.id)])
            open_amt = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
            ).mapped('amount_residual'))
            today = fields.Date.context_today(rec)
            overdue = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
                and m.invoice_date_due
                and m.invoice_date_due < today
            ).mapped('amount_residual'))
            rec.message_post(body=_(
                'Open: {o:.2f}, Overdue: {d:.2f} '
                '({c} posted invoice(s)).').format(
                o=open_amt, d=overdue, c=len(moves)))
        return True
