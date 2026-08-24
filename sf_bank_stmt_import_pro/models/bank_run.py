# -*- coding: utf-8 -*-
"""Bank statement import runs: parse preview, dedup, import to Odoo."""
import hashlib

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from .parsers import run_parser, ParseError


class SfBankStmtRun(models.Model):
    """One import run: file + template + journal -> statement."""
    _name = 'sf.bank.stmt.run'
    _description = 'Bank Statement Import Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Run Reference', required=True, copy=False,
                       readonly=True, default='New')
    template_id = fields.Many2one('sf.bank.stmt.template', string='Import Template',
                                  required=True)
    file_format = fields.Selection(related='template_id.file_format')
    journal_id = fields.Many2one('account.journal', string='Bank Journal',
                                 required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))])
    currency_id = fields.Many2one(related='journal_id.currency_id')
    company_id = fields.Many2one(related='journal_id.company_id', store=True)
    import_file = fields.Binary(string='Statement File', required=True,
                                attachment=True)
    file_name = fields.Char(string='File Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('parsed', 'Parsed - Review'),
        ('imported', 'Imported'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)
    line_ids = fields.One2many('sf.bank.stmt.line.preview', 'run_id',
                               string='Parsed Lines')
    statement_id = fields.Many2one('account.bank.statement',
                                   string='Created Statement', readonly=True,
                                   copy=False)
    skip_duplicates = fields.Boolean(string='Skip Duplicates', default=True,
                                     help='Uncheck to import flagged '
                                          'duplicates anyway.')
    total_lines = fields.Integer(compute='_compute_stats')
    duplicate_count = fields.Integer(compute='_compute_stats')
    error_count = fields.Integer(compute='_compute_stats')
    net_amount = fields.Monetary(string='Net Amount (parsed)',
                                 compute='_compute_stats',
                                 currency_field='currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.bank.stmt.run') or 'BIMP-NEW'
        return super().create(vals_list)

    def _compute_stats(self):
        for run in self:
            lines = run.line_ids
            run.total_lines = len(lines)
            run.duplicate_count = len(lines.filtered('is_duplicate'))
            run.error_count = len(lines.filtered('error_message'))
            run.net_amount = sum(l.amount for l in lines
                                 if not l.error_message)

    # ------------------------------------------------------------------
    # Parse
    # ------------------------------------------------------------------
    def action_parse_file(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft runs can parse a file.'))
        if not self.import_file:
            raise UserError(_('Upload a statement file first.'))
        raw = self.import_file
        try:
            result = run_parser(self.template_id, raw)
        except ParseError as exc:
            raise UserError(_('Parsing failed: %s') % exc)

        self.line_ids.unlink()
        existing_hashes = self._existing_hashes()
        seen_hashes = set()
        vals_list = []
        for line in result['lines']:
            line_hash = self._line_hash(line)
            is_dup = line_hash in existing_hashes or line_hash in seen_hashes
            seen_hashes.add(line_hash)
            vals_list.append({
                'run_id': self.id,
                'date': line['date'],
                'amount': line['amount'],
                'reference': line.get('reference') or '',
                'communication': line.get('communication') or '',
                'partner_name': line.get('partner_name') or '',
                'currency_code': line.get('currency') or '',
                'is_duplicate': is_dup,
                'line_hash': line_hash,
            })
        self.env['sf.bank.stmt.line.preview'].create(vals_list)
        self.write({'state': 'parsed'})
        self.message_post(body=_(
            'Parsed %(count)s lines (%(dups)s duplicates flagged) from %(file)s',
            count=len(vals_list),
            dups=sum(1 for v in vals_list if v['is_duplicate']),
            file=self.file_name or 'uploaded file'))

    def _line_hash(self, line):
        basis = '%s|%s|%.2f|%s' % (
            self.journal_id.id, line['date'], line['amount'],
            (line.get('reference') or '')[:80])
        return hashlib.sha256(basis.encode('utf-8')).hexdigest()

    def _existing_hashes(self):
        """Hashes of existing statement lines in this journal (lookback 180d)."""
        self.ensure_one()
        StatementLine = self.env['account.bank.statement.line']
        domain = [('journal_id', '=', self.journal_id.id)]
        lines = StatementLine.search(domain, limit=5000, order='date desc')
        hashes = set()
        for line in lines:
            basis = '%s|%s|%.2f|%s' % (
                self.journal_id.id, line.date, line.amount,
                (line.payment_ref or '')[:80])
            hashes.add(hashlib.sha256(basis.encode('utf-8')).hexdigest())
        return hashes

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------
    def action_import_lines(self):
        self.ensure_one()
        if self.state != 'parsed':
            raise UserError(_('Parse the file before importing.'))
        lines = self.line_ids
        if not lines:
            raise UserError(_('Nothing to import.'))
        to_import = lines.filtered(
            lambda l: not l.error_message
            and (self.skip_duplicates is False or not l.is_duplicate))
        if not to_import:
            raise UserError(_('All lines are duplicates or in error. '
                              'Uncheck "Skip Duplicates" to force import.'))

        dates = to_import.mapped('date')
        statement = self.env['account.bank.statement'].create({
            'journal_id': self.journal_id.id,
            'name': '%s %s -> %s' % (self.name, min(dates), max(dates)),
            'date': max(dates),
            'company_id': self.company_id.id,
        })
        created = self.env['account.bank.statement.line']
        for line in to_import:
            partner = self._resolve_partner(line.partner_name)
            currency = self._resolve_currency(line.currency_code)
            line_vals = {
                'statement_id': statement.id,
                'date': line.date,
                'amount': line.amount,
                'payment_ref': line.communication or line.reference
                or line.date.isoformat(),
                'partner_id': partner.id if partner else False,
            }
            if currency and currency != self.currency_id:
                line_vals['foreign_currency_id'] = currency.id
            created |= self.env['account.bank.statement.line'].create(line_vals)
            line.write({'imported': True})

        # Balances from parsers (MT940/CAMT) when available
        try:
            result = run_parser(self.template_id, self.import_file)
            if result.get('balance_start') or result.get('balance_end'):
                statement.write({
                    'balance_start': result.get('balance_start', 0.0),
                    'balance_end_real': result.get('balance_end', 0.0),
                })
        except ParseError:
            pass

        self.write({'state': 'imported', 'statement_id': statement.id})
        self.message_post(body=_(
            'Imported %s lines into statement %s (%s duplicates skipped).',
            len(created), statement.name,
            len(lines.filtered('is_duplicate'))))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bank Statement'),
            'res_model': 'account.bank.statement',
            'res_id': statement.id,
            'view_mode': 'form',
        }

    def _resolve_partner(self, name):
        if not name:
            return self.env['res.partner']
        return self.env['res.partner'].search(
            [('name', '=', name)], limit=1)

    def _resolve_currency(self, code):
        if not code or len(code) != 3:
            return self.env['res.currency']
        currency = self.env['res.currency'].search(
            [('name', '=', code.upper()), ('active', '=', True)], limit=1)
        return currency

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        if self.statement_id:
            raise UserError(_('Imported runs cannot go back to draft.'))
        self.write({'state': 'draft'})


class SfBankStmtLinePreview(models.Model):
    """Parsed line shown in the review grid before import."""
    _name = 'sf.bank.stmt.line.preview'
    _description = 'Bank Import Preview Line'
    _order = 'date, id'

    run_id = fields.Many2one('sf.bank.stmt.run', string='Import Run',
                             required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True)
    amount = fields.Float(string='Amount')
    reference = fields.Char(string='Reference')
    communication = fields.Char(string='Communication')
    partner_name = fields.Char(string='Partner (from file)')
    currency_code = fields.Char(string='Currency')
    is_duplicate = fields.Boolean(string='Duplicate?')
    line_hash = fields.Char()
    imported = fields.Boolean(string='Imported', default=False)
    error_message = fields.Char(string='Error')
    run_state = fields.Selection(related='run_id.state')
    currency_id = fields.Many2one(related='run_id.currency_id')
