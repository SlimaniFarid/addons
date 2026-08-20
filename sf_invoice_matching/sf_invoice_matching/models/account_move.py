# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    sf_match_state = fields.Selection([
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('matched', 'Matched'),
        ('exception', 'Exception'),
        ('resolved', 'Resolved'),
        ('payment_blocked', 'Payment Blocked'),
    ], string='3-Way Match Status', default='pending', required=True,
       tracking=True, index=True)
    sf_match_score = fields.Float(string='Match Score (%)',
                                  compute='_compute_match_score', store=True,
                                  group_operator='avg')
    sf_match_date = fields.Datetime(string='Last match run')
    sf_has_major_discrepancy = fields.Boolean(
        string='Has major discrepancy',
        compute='_compute_match_score', store=True)
    sf_match_line_ids = fields.One2many('sf.invoice.match.line', 'move_id',
                                        string='Match Lines')
    sf_match_log_ids = fields.One2many('sf.invoice.match.log', 'move_id',
                                       string='Match History')
    sf_match_exception_ids = fields.One2many('sf.invoice.exception',
                                             'move_id',
                                             string='Exceptions')

    @api.depends('sf_match_line_ids.status')
    def _compute_match_score(self):
        for move in self:
            lines = move.sf_match_line_ids
            if not lines:
                move.sf_match_score = 0.0
                move.sf_has_major_discrepancy = False
                continue
            total = len(lines)
            ok = len(lines.filtered(lambda l: l.status == 'ok'))
            move.sf_match_score = round(ok / float(total) * 100, 2)
            move.sf_has_major_discrepancy = bool(
                lines.filtered(lambda l: l.status == 'major'))

    # ------------------------------------------------------------------
    # Matching engine
    # ------------------------------------------------------------------
    def action_run_match(self):
        for move in self:
            move.sudo()._run_match()
        return {'type': 'ir.actions.act_window_close'}

    def action_recheck(self):
        return self.action_run_match()

    def _run_match(self):
        self.ensure_one()
        if self.move_type not in ('in_invoice', 'in_refund'):
            raise UserError(_('3-Way matching applies to vendor bills and '
                              'credit notes only.'))
        self.sf_match_line_ids.unlink()
        line_vals = []
        for line in self.invoice_line_ids:
            po_line = line.purchase_line_id
            if not po_line:
                continue
            received = po_line.move_ids.filtered(lambda m: m.state == 'done')
            qty_received = sum(received.mapped('product_uom_qty')) or 0.0
            price_ordered = po_line.price_unit
            if po_line.currency_id != self.currency_id:
                price_ordered = po_line.currency_id._convert(
                    po_line.price_unit, self.currency_id, self.company_id,
                    self.invoice_date or fields.Date.context_today(self))
            line_vals.append({
                'move_id': self.id,
                'move_line_id': line.id,
                'po_line_id': po_line.id,
                'stock_move_id': received[:1].id,
                'product_id': line.product_id.id,
                'qty_invoice': line.quantity,
                'qty_received': qty_received,
                'qty_ordered': po_line.product_qty,
                'price_invoice': line.price_unit,
                'price_ordered': price_ordered,
            })
        if not line_vals:
            self.sf_match_state = 'pending'
            self.sf_match_date = fields.Datetime.now()
            self._log_match('pending', _('No purchase order lines linked '
                                         'to this invoice.'))
            return
        self.env['sf.invoice.match.line'].create(line_vals)
        self.sf_match_date = fields.Datetime.now()
        self._evaluate_match()

    def _evaluate_match(self):
        self.ensure_one()
        lines = self.sf_match_line_ids
        has_major = lines.filtered(lambda l: l.status == 'major')
        has_minor = lines.filtered(lambda l: l.status == 'minor')
        company = self.company_id
        partner = self.partner_id
        total_invoice = sum(self.invoice_line_ids.mapped('price_subtotal'))
        total_ordered = sum(
            lines.mapped(lambda l: l.qty_ordered * l.price_ordered))
        total_pct = abs(total_invoice - total_ordered) / (
            total_ordered or 1.0) * 100
        total_tolerance = partner.sf_match_tolerance_total_pct \
            if partner.sf_match_tolerance_total_pct >= 0 \
            else company.sf_match_tolerance_total_pct
        total_exceeds = total_pct > total_tolerance

        if has_major or total_exceeds:
            open_exception = self.sf_match_exception_ids.filtered(
                lambda e: e.state in ('open', 'rejected')
                and e.severity == 'major')
            if not open_exception:
                self.env['sf.invoice.exception'].create({
                    'move_id': self.id,
                    'severity': 'major',
                    'description': _('Major discrepancy detected on invoice '
                                     '%s (quantity, price or total out of '
                                     'tolerance).') % self.name,
                })
            self.sf_match_state = 'exception'
            self._log_match('major', _('Major discrepancy: %s line(s) out '
                                       'of tolerance.') % len(has_major))
            self._notify_ap_manager(
                _('3-Way Match: invoice %s is in exception') % self.name)
            return 'major'
        if has_minor:
            self._resolve_open_exceptions()
            self.sf_match_state = 'matched'
            self._log_match('minor', _('Minor differences within tolerance.'))
            return 'minor'
        self._resolve_open_exceptions()
        self.sf_match_state = 'matched'
        self._log_match('matched', _('Invoice is within tolerances.'))
        return 'matched'

    def _resolve_open_exceptions(self):
        open_exc = self.sf_match_exception_ids.filtered(
            lambda e: e.state in ('open', 'rejected'))
        if open_exc:
            open_exc.write({
                'state': 'arbitrated',
                'decision': 'accept',
                'decision_date': fields.Datetime.now(),
                'decision_note': _('Auto-resolved: recheck passed.'),
            })
            self.sf_match_state = 'resolved'

    def _log_match(self, result, details):
        self.env['sf.invoice.match.log'].create({
            'move_id': self.id,
            'result': result,
            'details': details,
        })

    def _sf_has_open_major_exception(self):
        self.ensure_one()
        return bool(self.sf_match_exception_ids.filtered(
            lambda e: e.state in ('open', 'rejected')
            and e.severity == 'major'))

    def _check_sf_not_blocked(self):
        self.ensure_one()
        if self._sf_has_open_major_exception():
            raise UserError(
                _('This invoice has an unresolved major discrepancy. '
                  'Arbitrate the exception before validating or paying.'))

    def _notify_ap_manager(self, summary):
        group = self.env.ref(
            'sf_invoice_matching.group_invoice_matching_manager')
        managers = self.env['res.users'].search([
            ('groups_id', 'in', group.id),
            ('share', '=', False),
        ], limit=1)
        if managers:
            self.activity_schedule('mail.mail_activity_data_todo',
                                   summary=summary,
                                   user_id=managers.id)

    def _check_sf_exceptions(self):
        moves = self.search([('sf_match_state', '=', 'exception')])
        for move in moves:
            if move.sf_match_exception_ids.filtered(
                    lambda e: e.state == 'open'):
                move._run_match()
                open_exc = move.sf_match_exception_ids.filtered(
                    lambda e: e.state == 'open')
                if open_exc:
                    responsible = open_exc[:1].responsible_id
                    if responsible:
                        move.activity_schedule(
                            'mail.mail_activity_data_todo',
                            summary=_('3-Way Match: unresolved exception on '
                                      '%s') % move.name,
                            user_id=responsible.id)

    # ------------------------------------------------------------------
    # Accounting overrides
    # ------------------------------------------------------------------
    def action_post(self):
        for move in self:
            if (move.move_type in ('in_invoice', 'in_refund')
                    and move.invoice_line_ids.filtered('purchase_line_id')):
                if move.sf_match_state != 'exception':
                    move.sudo()._run_match()
                move._check_sf_not_blocked()
        return super().action_post()

    def action_register_payment(self):
        for move in self:
            move._check_sf_not_blocked()
        return super().action_register_payment()

    def action_force_register_payment(self):
        for move in self:
            move._check_sf_not_blocked()
        return super().action_force_register_payment()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sf_match_line_ids = fields.One2many('sf.invoice.match.line',
                                        'move_line_id',
                                        string='Match Lines')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sf_match_line_ids = fields.One2many('sf.invoice.match.line',
                                        'po_line_id',
                                        string='Match Lines')