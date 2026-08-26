# -*- coding: utf-8 -*-
"""Supplier rebate deals, accruals and claims."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierRebateDeal(models.Model):
    _name = 'sf.supplier.rebate.deal'
    _description = 'Supplier Rebate Deal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc'

    name = fields.Char(string='Deal Reference', required=True, copy=False,
                       readonly=True, default='New')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True,
                                domain=[('supplier_rank', '>', 0)])
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    date_start = fields.Date(string='Period Start', required=True)
    date_end = fields.Date(string='Period End', required=True)
    deal_type = fields.Selection([
        ('turnover_bonus', 'Turnover Bonus (fixed above threshold)'),
        ('retro_percent', 'Retro-discount % on purchases'),
        ('per_unit', 'Fixed Rebate per Unit')],
        required=True, default='retro_percent')
    product_category_id = fields.Many2one(
        'product.category', string='Product Category Scope',
        help='Empty = all categories.')
    threshold_amount = fields.Monetary(string='Purchase Threshold',
                                       help='Turnover bonus only.')
    rebate_percent = fields.Float(string='Rebate %')
    rebate_per_unit = fields.Monetary(string='Rebate per Unit')
    fixed_bonus_amount = fields.Monetary(string='Fixed Bonus Amount')
    state = fields.Selection([
        ('draft', 'Draft'), ('active', 'Active'), ('claimed', 'Claimed'),
        ('settled', 'Settled'), ('expired', 'Expired')],
        default='draft', tracking=True)
    accrual_ids = fields.One2many('sf.supplier.rebate.accrual', 'deal_id',
                                  string='Accruals')
    claim_ids = fields.One2many('sf.supplier.rebate.claim', 'deal_id',
                                string='Claims')
    total_purchases = fields.Float(string='Purchases in Period',
                                   compute='_compute_totals')
    total_accrued = fields.Float(string='Total Accrued',
                                 compute='_compute_totals')
    progress_percent = fields.Float(string='Threshold Progress %',
                                    compute='_compute_totals')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.rebate.deal') or 'SRB-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for deal in self:
            domain = [
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', deal.vendor_id.id),
                ('invoice_date', '>=', deal.date_start),
                ('invoice_date', '<=', deal.date_end),
                ('company_id', '=', deal.company_id.id),
            ]
            invoices = self.env['account.move'].search(domain)
            purchases = 0.0
            units = 0
            for inv in invoices:
                for line in inv.invoice_line_ids.filtered(
                        lambda l: not l.display_type):
                    if (deal.product_category_id
                            and line.product_id.categ_id
                            != deal.product_category_id):
                        continue
                    purchases += line.price_subtotal
                    units += line.quantity
            deal.total_purchases = purchases
            deal.total_accrued = sum(a.accrued_amount
                                     for a in deal.accrual_ids)
            deal.progress_percent = (purchases / deal.threshold_amount * 100.0
                                     if deal.threshold_amount else 0.0)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_compute_accrual(self):
        """Create/refresh one accrual per month of the deal period."""
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active deals can compute accruals.'))
        self.accrual_ids.filtered(
            lambda a: not a.claimed).unlink()
        import dateutil.relativedelta as rd
        current = self.date_start.replace(day=1)
        vals_list = []
        while current <= self.date_end:
            month_end = (current + rd.relativedelta(months=1, days=-1))
            domain = [
                ('move_type', '=', 'in_invoice'), ('state', '=', 'posted'),
                ('partner_id', '=', self.vendor_id.id),
                ('invoice_date', '>=', current),
                ('invoice_date', '<=', min(month_end, self.date_end)),
                ('company_id', '=', self.company_id.id),
            ]
            invoices = self.env['account.move'].search(domain)
            purchases = 0.0
            units = 0.0
            for inv in invoices:
                for line in inv.invoice_line_ids.filtered(
                        lambda l: not l.display_type):
                    if (self.product_category_id
                            and line.product_id.categ_id
                            != self.product_category_id):
                        continue
                    purchases += line.price_subtotal
                    units += line.quantity
            if self.deal_type == 'retro_percent':
                amount = purchases * self.rebate_percent / 100.0
            elif self.deal_type == 'per_unit':
                amount = units * self.rebate_per_unit
            else:
                amount = 0.0
            vals_list.append({
                'deal_id': self.id,
                'period_month': current,
                'purchases': purchases,
                'units': units,
                'accrued_amount': amount,
            })
            current = current + rd.relativedelta(months=1)
        if vals_list:
            self.env['sf.supplier.rebate.accrual'].create(vals_list)


class SfSupplierRebateAccrual(models.Model):
    _name = 'sf.supplier.rebate.accrual'
    _description = 'Supplier Rebate Accrual'

    deal_id = fields.Many2one('sf.supplier.rebate.deal', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one(related='deal_id.company_id', store=True)
    currency_id = fields.Many2one(related='deal_id.currency_id')
    period_month = fields.Date(string='Month')
    purchases = fields.Float(string='Purchases')
    units = fields.Float(string='Units')
    accrued_amount = fields.Float(string='Accrued Rebate')
    claimed = fields.Boolean(default=False)


class SfSupplierRebateClaim(models.Model):
    _name = 'sf.supplier.rebate.claim'
    _description = 'Supplier Rebate Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Claim Reference', required=True, copy=False,
                       readonly=True, default='New')
    deal_id = fields.Many2one('sf.supplier.rebate.deal', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one(related='deal_id.company_id', store=True)
    currency_id = fields.Many2one(related='deal_id.currency_id')
    claim_date = fields.Date(string='Claim Date', required=True,
                             default=fields.Date.today)
    claimed_amount = fields.Monetary(string='Claimed Amount', required=True)
    credit_note_ref = fields.Char(string='Vendor Credit Note Ref')
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('received', 'Credit Received'), ('disputed', 'Disputed')],
        default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.rebate.claim') or 'SRC-NEW'
            vals['deal_id'] = vals.get('deal_id')
        res = super().create(vals_list)
        res.mapped('deal_id').write({'state': 'claimed'})
        return res

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_mark_received(self):
        for rec in self:
            if not rec.credit_note_ref:
                raise UserError(_('Enter the vendor credit note reference.'))
            rec.write({'state': 'received'})
            rec.deal_id.write({'state': 'settled'})

    def action_dispute(self):
        self.write({'state': 'disputed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier.rebate.deal'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('claim_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.claim_date
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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.supplier.rebate.deal'

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
