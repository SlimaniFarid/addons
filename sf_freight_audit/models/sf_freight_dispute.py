# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfFreightDispute(models.Model):
    _name = 'sf.freight.dispute'
    _description = 'Freight Carrier Dispute'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    invoice_id = fields.Many2one('sf.freight.invoice', string='Invoice',
                                 required=True, ondelete='restrict',
                                 index=True)
    carrier_id = fields.Many2one(related='invoice_id.carrier_id',
                                 store=True)
    finding_ids = fields.One2many('sf.freight.finding', 'dispute_id',
                                  string='Findings')
    amount_claimed = fields.Monetary(
        string='Amount Claimed', currency_field='currency_id',
        compute='_compute_amount_claimed', store=True)
    currency_id = fields.Many2one(related='invoice_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Carrier'),
        ('carrier_response', 'Carrier Responded'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True, copy=False,
        index=True)
    resolution_type = fields.Selection([
        ('credit_note', 'Credit Note Received'),
        ('refund', 'Refund Received'),
        ('rejected', 'Rejected by Carrier'),
        ('waived', 'Waived by Us'),
    ], string='Resolution')
    credit_note_id = fields.Many2one('account.move', string='Credit Note',
                                     ondelete='set null', readonly=True,
                                     copy=False)
    carrier_response = fields.Text(string='Carrier Response')
    response_date = fields.Date(string='Response Date')
    resolved_date = fields.Date(string='Resolved Date')
    user_id = fields.Many2one('res.users', string='Responsible',
                              default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    @api.depends('finding_ids.status', 'finding_ids.variance_amount')
    def _compute_amount_claimed(self):
        for d in self:
            findings = d.finding_ids.filtered(
                lambda f: f.status != 'waived')
            d.amount_claimed = sum(abs(f.variance_amount)
                                   for f in findings)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.freight.dispute') or _('New')
            if not vals.get('finding_ids'):
                raise UserError(_('A dispute requires at least one '
                                  'finding.'))
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals:
            flow = {
                'draft': {'draft', 'submitted'},
                'submitted': {'submitted', 'carrier_response'},
                'carrier_response': {'carrier_response', 'resolved'},
                'resolved': {'resolved', 'closed'},
                'closed': {'closed'},
            }
            for rec in self:
                if vals['state'] not in flow.get(rec.state, set()):
                    raise UserError(_(
                        'Invalid dispute transition %s -> %s.')
                        % (rec.state, vals['state']))
        return super().write(vals)

    def unlink(self):
        if any(rec.state != 'draft' for rec in self):
            raise UserError(_('Only draft disputes can be deleted.'))
        return super().unlink()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_submit(self):
        for d in self:
            if d.state != 'draft':
                raise UserError(_('Only draft disputes can be submitted.'))
            d.finding_ids.write({'status': 'disputed'})
            d.invoice_id.sudo().write({'state': 'disputed'})
            d.state = 'submitted'
            d.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_('Awaiting carrier response'),
                note=_('Dispute %s submitted to %s.')
                % (d.name, d.carrier_id.name),
                date_deadline=fields.Date.today() + timedelta(days=10),
            )

    def action_carrier_responded(self):
        for d in self:
            if d.state != 'submitted':
                raise UserError(_('No pending submission.'))
            d.state = 'carrier_response'

    def action_resolve_credit_note(self):
        """Generate a vendor credit note and reconcile it."""
        for d in self:
            if d.state != 'carrier_response':
                raise UserError(_(
                    'Resolve only from carrier_response state.'))
            if not d.amount_claimed:
                raise UserError(_('Nothing to claim.'))
            journal = self.env['account.journal'].search([
                ('company_id', '=', d.company_id.id),
                ('type', '=', 'purchase'),
            ], limit=1)
            if not journal:
                raise UserError(_('No purchase journal found.'))
            account = self.env['account.account'].search([
                ('account_type', '=', 'expense'),
                ('company_id', '=', d.company_id.id),
            ], limit=1)
            move = self.env['account.move'].create({
                'move_type': 'in_refund',
                'partner_id': d.carrier_id.id,
                'invoice_date': fields.Date.context_today(self),
                'journal_id': journal.id,
                'company_id': d.company_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': _('Freight overcharge recovery - %s') % d.name,
                    'quantity': 1,
                    'price_unit': d.amount_claimed,
                    'account_id': account.id if account else False,
                })],
            })
            move.action_post()
            d.credit_note_id = move.id
            d.resolution_type = 'credit_note'
            d.resolved_date = fields.Date.today()
            d.finding_ids.write({'status': 'resolved'})
            d.state = 'resolved'
            inv = d.invoice_id
            if not inv.finding_ids.filtered(lambda f: f.status == 'open'):
                inv.write({'state': 'resolved'})

    def action_reject(self):
        for d in self:
            d.resolution_type = 'rejected'
            d.resolved_date = fields.Date.today()
            d.finding_ids.write({'status': 'explained'})
            d.state = 'resolved'

    def action_close(self):
        for d in self:
            if d.state != 'resolved':
                raise UserError(_('Close only resolved disputes.'))
            d.state = 'closed'

    # ------------------------------------------------------------------
    # Cron
    # ------------------------------------------------------------------
    @api.model
    def _cron_dispute_escalation(self):
        todo = self.env.ref('mail.mail_activity_data_todo',
                            raise_if_not_found=False)
        deadline_warn = fields.Date.today() - timedelta(days=10)
        companies = self.env['res.company'].search([])
        for company in companies:
            disputes = self.with_company(company).search([
                ('state', '=', 'submitted'),
                ('company_id', '=', company.id),
                ('write_date', '<', deadline_warn),
            ])
            for d in disputes:
                existing = self.env['mail.activity'].search([
                    ('res_model', '=', self._name),
                    ('res_id', '=', d.id),
                    ('done', '=', False),
                ], limit=1)
                if existing:
                    continue
                d.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=d.user_id.id or self.env.user.id,
                    summary=_('Carrier response overdue'),
                    note=_('Dispute %s has been awaiting response '
                           'for more than 10 days.') % d.name,
                )
