# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

SEQUENCE_PREFIX = {
    'import_lc': 'LC',
    'export_lc': 'ELC',
    'bank_guarantee': 'BG',
    'documentary_collection': 'DC',
}


class TradeInstrument(models.Model):
    _name = 'sf.trade.instrument'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Trade Finance Instrument'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    instrument_type = fields.Selection([
        ('import_lc', 'Import Letter of Credit'),
        ('export_lc', 'Export Letter of Credit'),
        ('bank_guarantee', 'Bank Guarantee'),
        ('documentary_collection', 'Documentary Collection'),
    ], string='Type', required=True, tracking=True)
    direction = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export'),
    ], string='Direction', required=True)
    bank_id = fields.Many2one('sf.trade.bank', string='Bank', required=True,
                              ondelete='restrict')
    counterparty_id = fields.Many2one('res.partner',
                                      string='Counterparty', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True,
                                  default=lambda self: self.env.company.currency_id)
    amount = fields.Monetary(string='Amount', currency_field='currency_id',
                             required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('issued', 'Issued'),
        ('active', 'Active'),
        ('settled', 'Settled'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    application_date = fields.Date(string='Application date')
    issue_date = fields.Date(string='Issue date')
    expiry_date = fields.Date(string='Expiry date', index=True)
    payment_date = fields.Date(string='Payment date')
    order_ids = fields.Many2many('purchase.order',
                                 string='Purchase orders')
    invoice_ids = fields.Many2many('account.move', string='Invoices')
    document_ids = fields.One2many('sf.trade.instrument.document',
                                   'instrument_id', string='Documents')
    fee_ids = fields.One2many('sf.trade.instrument.fee', 'instrument_id',
                              string='Bank fees')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('An instrument with this number already exists.')),
        ('amount_positive', 'CHECK(amount >= 0)',
         _('The amount cannot be negative.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            prefix = SEQUENCE_PREFIX.get(vals.get('instrument_type'), 'TF')
            seq = self.env['ir.sequence'].next_by_code('sf.trade.instrument')
            vals['name'] = '%s-%s' % (prefix, seq)
        return super().create(vals)

    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for instrument in self:
            if (instrument.issue_date and instrument.expiry_date
                    and instrument.expiry_date < instrument.issue_date):
                raise ValidationError(_('The expiry date cannot be before '
                                        'the issue date.'))

    def _check_documents_accepted(self):
        self.ensure_one()
        pending = self.document_ids.filtered(
            lambda d: d.state != 'accepted')
        if pending:
            raise UserError(_('All required documents must be accepted '
                              'before settling this instrument.'))

    def action_request(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft instruments can be requested.'))
        self.state = 'requested'
        if not self.application_date:
            self.application_date = fields.Date.context_today(self)

    def action_issue(self):
        self.ensure_one()
        if self.state != 'requested':
            raise UserError(_('Only requested instruments can be issued.'))
        self.state = 'issued'
        if not self.issue_date:
            self.issue_date = fields.Date.context_today(self)

    def action_activate(self):
        self.ensure_one()
        if self.state != 'issued':
            raise UserError(_('Only issued instruments can be activated.'))
        self.state = 'active'

    def action_settle(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_trade_finance.group_trade_manager'):
            raise UserError(_('Only trade finance managers can settle '
                              'instruments.'))
        if self.state != 'active':
            raise UserError(_('Only active instruments can be settled.'))
        self._check_documents_accepted()
        self.state = 'settled'
        if not self.payment_date:
            self.payment_date = fields.Date.context_today(self)

    def action_close(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_trade_finance.group_trade_manager'):
            raise UserError(_('Only trade finance managers can close '
                              'instruments.'))
        if self.state != 'settled':
            raise UserError(_('Only settled instruments can be closed.'))
        self.state = 'closed'

    def action_cancel(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_trade_finance.group_trade_manager'):
            raise UserError(_('Only trade finance managers can cancel '
                              'instruments.'))
        if self.state not in ('draft', 'requested'):
            raise UserError(_('Only draft or requested instruments can be '
                              'cancelled.'))
        return {
            'name': _('Cancel Instrument'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.trade.instrument.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_instrument_id': self.id},
        }

    def unlink(self):
        for instrument in self:
            if instrument.state in ('active', 'settled'):
                raise UserError(_('An active or settled instrument cannot be '
                                  'deleted. Archive it instead.'))
        return super().unlink()

    def _check_trade_expiry_alerts(self):
        today = fields.Date.today()
        for instrument in self.search([('state', '=', 'active')]):
            if not instrument.expiry_date:
                continue
            days_left = (instrument.expiry_date - today).days
            if 0 <= days_left <= instrument.company_id.sf_trade_alert_days:
                group = self.env.ref(
                    'sf_trade_finance.group_trade_manager')
                treasurers = self.env['res.users'].search([
                    ('groups_id', 'in', group.id),
                    ('share', '=', False),
                ], limit=1)
                if treasurers:
                    instrument.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Instrument %s expires on %s')
                        % (instrument.name, instrument.expiry_date),
                        user_id=treasurers.id)


class TradeInstrumentDocument(models.Model):
    _name = 'sf.trade.instrument.document'
    _description = 'Trade Instrument Document'
    _order = 'instrument_id, id'

    instrument_id = fields.Many2one('sf.trade.instrument',
                                    string='Instrument', required=True,
                                    ondelete='cascade', index=True)
    name = fields.Char(string='Document', required=True,
                       help='e.g. Bill of Lading, Commercial Invoice, '
                            'Certificate of Origin')
    state = fields.Selection([
        ('required', 'Required'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Status', default='required', required=True)
    submitted_on = fields.Date(string='Submitted on')
    accepted_on = fields.Date(string='Accepted on')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='instrument_id.company_id',
                                 store=True, readonly=True)

    def action_submit(self):
        self.ensure_one()
        self.state = 'submitted'
        self.submitted_on = fields.Date.context_today(self)

    def action_accept(self):
        self.ensure_one()
        self.state = 'accepted'
        self.accepted_on = fields.Date.context_today(self)

    def action_reject(self):
        self.ensure_one()
        self.state = 'rejected'


class TradeInstrumentFee(models.Model):
    _name = 'sf.trade.instrument.fee'
    _description = 'Trade Instrument Bank Fee'
    _order = 'instrument_id, fee_date'

    instrument_id = fields.Many2one('sf.trade.instrument',
                                    string='Instrument', required=True,
                                    ondelete='cascade', index=True)
    fee_type = fields.Selection([
        ('issue', 'Issue'),
        ('amendment', 'Amendment'),
        ('negotiation', 'Negotiation'),
        ('presentation', 'Presentation'),
        ('dispatch', 'Dispatch'),
        ('other', 'Other'),
    ], string='Fee type')
    amount = fields.Monetary(string='Amount', currency_field='currency_id',
                             required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True,
                                  default=lambda self: self.env.company.currency_id)
    fee_date = fields.Date(string='Date', required=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='instrument_id.company_id',
                                 store=True, readonly=True)

    _sql_constraints = [
        ('amount_positive', 'CHECK(amount >= 0)',
         _('The fee amount cannot be negative.')),
    ]


class TradeBank(models.Model):
    _name = 'sf.trade.bank'
    _description = 'Trade Finance Bank'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    swift = fields.Char(string='SWIFT / BIC')
    branch = fields.Char(string='Branch')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This bank already exists.')),
    ]


class TradeInstrumentCancelWizard(models.TransientModel):
    _name = 'sf.trade.instrument.cancel.wizard'
    _description = 'Cancel Instrument'

    instrument_id = fields.Many2one('sf.trade.instrument',
                                    string='Instrument', required=True)
    reason = fields.Text(string='Cancellation reason', required=True)

    def action_confirm(self):
        self.ensure_one()
        instrument = self.instrument_id
        if not self.env.user.has_group('sf_trade_finance.group_trade_manager'):
            raise UserError(_('Only trade finance managers can cancel '
                              'instruments.'))
        if instrument.state not in ('draft', 'requested'):
            raise UserError(_('Only draft or requested instruments can be '
                              'cancelled.'))
        instrument.state = 'cancelled'
        instrument.notes = (instrument.notes or '') + '\n' + _(
            'Cancelled: %s') % self.reason
        return {'type': 'ir.actions.act_window_close'}

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.trade.instrument'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
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
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

