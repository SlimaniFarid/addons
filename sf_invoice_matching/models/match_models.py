# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError


class InvoiceMatchLine(models.Model):
    _name = 'sf.invoice.match.line'
    _description = 'Invoice 3-Way Match Line'
    _order = 'move_id, id'

    move_id = fields.Many2one('account.move', string='Invoice',
                              required=True, ondelete='cascade', index=True)
    move_line_id = fields.Many2one('account.move.line', string='Invoice line',
                                   ondelete='cascade')
    po_line_id = fields.Many2one('purchase.order.line',
                                 string='Purchase order line',
                                 ondelete='cascade')
    stock_move_id = fields.Many2one('stock.move', string='Receipt',
                                    ondelete='set null')
    product_id = fields.Many2one('product.product', string='Product')
    qty_invoice = fields.Float(string='Invoiced qty')
    qty_received = fields.Float(string='Received qty')
    qty_ordered = fields.Float(string='Ordered qty')
    price_invoice = fields.Float(string='Invoice price')
    price_ordered = fields.Float(string='Order price')
    tax_diff = fields.Float(string='Tax diff', default=0.0)
    discount_diff = fields.Float(string='Discount diff', default=0.0)
    currency_id = fields.Many2one('res.currency',
                                  related='move_id.currency_id',
                                  readonly=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='move_id.company_id', store=True,
                                 readonly=True)
    qty_diff = fields.Float(string='Qty diff',
                            compute='_compute_diffs', store=True)
    price_diff_pct = fields.Float(string='Price diff (%)',
                                  compute='_compute_diffs', store=True)
    status = fields.Selection([
        ('ok', 'OK'),
        ('minor', 'Minor'),
        ('major', 'Major'),
    ], string='Status', compute='_compute_diffs', store=True)

    @api.depends('qty_invoice', 'qty_received', 'price_invoice',
                 'price_ordered', 'tax_diff', 'discount_diff',
                 'move_id.company_id.sf_match_tolerance_qty',
                 'move_id.company_id.sf_match_tolerance_price_pct',
                 'move_id.partner_id.sf_match_tolerance_qty',
                 'move_id.partner_id.sf_match_tolerance_price_pct')
    def _compute_diffs(self):
        for line in self:
            line.qty_diff = abs(line.qty_invoice - line.qty_received)
            if line.price_ordered:
                line.price_diff_pct = abs(
                    line.price_invoice - line.price_ordered) / \
                    line.price_ordered * 100
            else:
                line.price_diff_pct = 0.0
            tolerance_qty = line.move_id.partner_id.sf_match_tolerance_qty \
                if line.move_id.partner_id.sf_match_tolerance_qty >= 0 \
                else line.move_id.company_id.sf_match_tolerance_qty
            tolerance_price = line.move_id.partner_id.sf_match_tolerance_price_pct \
                if line.move_id.partner_id.sf_match_tolerance_price_pct >= 0 \
                else line.move_id.company_id.sf_match_tolerance_price_pct
            exceeds = (line.qty_diff > tolerance_qty
                       or line.price_diff_pct > tolerance_price
                       or line.tax_diff
                       or line.discount_diff)
            non_zero = (line.qty_diff or line.price_diff_pct
                        or line.tax_diff or line.discount_diff)
            if exceeds:
                line.status = 'major'
            elif non_zero:
                line.status = 'minor'
            else:
                line.status = 'ok'


class InvoiceMatchLog(models.Model):
    _name = 'sf.invoice.match.log'
    _description = 'Invoice Match History'
    _order = 'run_date desc, id desc'

    move_id = fields.Many2one('account.move', string='Invoice',
                              required=True, ondelete='cascade', index=True)
    run_date = fields.Datetime(string='Run date', default=fields.Datetime.now,
                               required=True)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.user)
    result = fields.Selection([
        ('matched', 'Matched'),
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('pending', 'Pending'),
    ], string='Result', required=True)
    details = fields.Text(string='Details')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='move_id.company_id', store=True,
                                 readonly=True)


class InvoiceException(models.Model):
    _name = 'sf.invoice.exception'
    _description = 'Invoice Matching Exception'
    _order = 'id desc'

    move_id = fields.Many2one('account.move', string='Invoice', required=True,
                              ondelete='cascade', index=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('arbitrated', 'Arbitrated'),
        ('rejected', 'Rejected'),
    ], string='Status', default='open', required=True, tracking=True)
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
    ], string='Severity', required=True)
    description = fields.Text(string='Description', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    decision = fields.Selection([
        ('accept', 'Accept discrepancy'),
        ('revise', 'Revise invoice'),
    ], string='Decision')
    decision_date = fields.Datetime(string='Decision date')
    decision_note = fields.Text(string='Decision note')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='move_id.company_id', store=True,
                                 readonly=True)

    def action_arbitrate(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_invoice_matching.group_invoice_matching_manager'):
            raise AccessError(_('Only matching managers can arbitrate '
                                'exceptions.'))
        if self.state != 'open':
            raise UserError(_('Only open exceptions can be arbitrated.'))
        return {
            'name': _('Arbitrate Exception'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.invoice.exception.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_exception_id': self.id},
        }

    def unlink(self):
        if self.filtered(lambda e: e.state in ('arbitrated', 'rejected')):
            raise UserError(_('Arbitrated or rejected exceptions cannot be '
                              'deleted; they are kept for audit.'))
        return super().unlink()


class InvoiceRunMatchWizard(models.TransientModel):
    _name = 'sf.invoice.run.match.wizard'
    _description = 'Run 3-Way Match'

    move_ids = fields.Many2many('account.move', string='Invoices')

    def action_run(self):
        self.move_ids.action_run_match()
        return {'type': 'ir.actions.act_window_close'}


class InvoiceExceptionWizard(models.TransientModel):
    _name = 'sf.invoice.exception.wizard'
    _description = 'Arbitrate Exception'

    exception_id = fields.Many2one('sf.invoice.exception',
                                   string='Exception', required=True)
    decision = fields.Selection([
        ('accept', 'Accept discrepancy'),
        ('revise', 'Revise invoice'),
    ], string='Decision', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    decision_note = fields.Text(string='Decision note', required=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_invoice_matching.group_invoice_matching_manager'):
            raise AccessError(_('Only matching managers can arbitrate '
                                'exceptions.'))
        exception = self.exception_id
        move = exception.move_id
        if self.decision == 'accept' and not self.responsible_id:
            raise UserError(_('A responsible user is required to accept a '
                              'discrepancy.'))
        exception.write({
            'decision': self.decision,
            'responsible_id': self.responsible_id.id,
            'decision_date': fields.Datetime.now(),
            'decision_note': self.decision_note,
        })
        if self.decision == 'accept':
            exception.state = 'arbitrated'
            if not move.sf_match_exception_ids.filtered(
                    lambda e: e.state in ('open', 'rejected')):
                move.sf_match_state = 'resolved'
        else:
            exception.state = 'rejected'
            move.sf_match_state = 'exception'
        return {'type': 'ir.actions.act_window_close'}