# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError

CHARGE_TYPES = [
    ('base_freight', 'Base Freight'),
    ('fuel_surcharge', 'Fuel Surcharge'),
    ('security', 'Security Fee'),
    ('residential', 'Residential Delivery'),
    ('liftgate', 'Liftgate'),
    ('insurance', 'Insurance'),
    ('customs', 'Customs Handling'),
    ('accessorial_other', 'Other Accessorial'),
    ('other', 'Other'),
]


class SfFreightInvoice(models.Model):
    _name = 'sf.freight.invoice'
    _description = 'Freight Carrier Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'invoice_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    carrier_id = fields.Many2one('res.partner', string='Carrier',
                                 required=True, ondelete='restrict',
                                 domain=[('is_company', '=', True)])
    contract_id = fields.Many2one('sf.freight.carrier.contract',
                                  string='Contract', ondelete='set null',
                                  domain="[('partner_id', '=', carrier_id),"
                                         " ('state', '=', 'active')]")
    invoice_ref = fields.Char(string='Carrier Invoice Number',
                              required=True)
    invoice_date = fields.Date(string='Invoice Date',
                               default=fields.Date.today)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.company.currency_id)
    source = fields.Selection([
        ('csv', 'CSV Import'),
        ('manual', 'Manual Entry'),
    ], string='Source', default='manual')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('imported', 'Imported'),
        ('matched', 'Matched'),
        ('validated', 'Validated'),
        ('discrepancy', 'Discrepancy'),
        ('disputed', 'Disputed'),
        ('resolved', 'Resolved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False,
        index=True)
    line_ids = fields.One2many('sf.freight.invoice.line', 'invoice_id',
                               string='Lines', copy=True)
    finding_ids = fields.One2many('sf.freight.finding', 'invoice_id',
                                  string='Findings')
    dispute_ids = fields.One2many('sf.freight.dispute', 'invoice_id',
                                  string='Disputes')
    open_finding_count = fields.Integer(
        string='Open Findings',
        compute='_compute_counts', store=True)
    total_declared = fields.Monetary(
        string='Total Billed', currency_field='currency_id',
        compute='_compute_totals', store=True)
    total_expected = fields.Monetary(
        string='Total Expected', currency_field='currency_id',
        compute='_compute_totals', store=True)
    total_variance = fields.Monetary(
        string='Total Variance', currency_field='currency_id',
        compute='_compute_totals', store=True,
        help='Billed minus expected. Positive means overbilled.')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('sf_freight_invoice_uniq',
         'unique(carrier_id, invoice_ref, company_id)',
         'This carrier invoice number already exists for this carrier.'),
    ]

    @api.depends('line_ids.amount_billed', 'line_ids.amount_expected')
    def _compute_totals(self):
        for inv in self:
            lines = inv.line_ids.filtered(
                lambda l: l.status != 'excluded')
            inv.total_declared = sum(lines.mapped('amount_billed'))
            inv.total_expected = sum(lines.mapped('amount_expected'))
            inv.total_variance = (inv.total_declared
                                  - inv.total_expected)

    @api.depends('finding_ids.status')
    def _compute_counts(self):
        for inv in self:
            inv.open_finding_count = len(inv.finding_ids.filtered(
                lambda f: f.status == 'open'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.freight.invoice') or _('New')
            if vals.get('state', 'draft') not in ('draft', 'imported'):
                raise UserError(_(
                    'Invoices can only be created as draft or imported.'))
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals:
            flow = {
                'draft': {'draft', 'imported', 'cancelled'},
                'imported': {'imported', 'matched', 'validated',
                             'discrepancy', 'cancelled'},
                'matched': {'matched', 'validated', 'discrepancy',
                            'cancelled'},
                'validated': {'validated', 'paid'},
                'discrepancy': {'discrepancy', 'disputed', 'resolved',
                                'cancelled'},
                'disputed': {'disputed', 'resolved', 'cancelled'},
                'resolved': {'resolved', 'paid'},
                'paid': {'paid'},
                'cancelled': {'cancelled'},
            }
            for rec in self:
                if vals['state'] not in flow.get(rec.state, set()):
                    raise UserError(_(
                        'Invalid invoice transition %s -> %s.')
                        % (rec.state, vals['state']))
        locked = self.filtered(
            lambda r: r.state not in ('draft', 'imported', 'cancelled'))
        if locked and any(f in vals for f in (
                'carrier_id', 'invoice_ref', 'invoice_date',
                'line_ids')):
            raise UserError(_(
                'A processed invoice cannot be edited. Cancel it instead.'))
        return super().write(vals)

    def unlink(self):
        if any(rec.state not in ('draft', 'cancelled') for rec in self):
            raise UserError(_('Only draft or cancelled invoices can be '
                              'deleted.'))
        return super().unlink()

    # ------------------------------------------------------------------
    # Engine
    # ------------------------------------------------------------------
    def action_run_audit(self):
        """Run the verification engine on all lines of these invoices."""
        Finding = self.env['sf.freight.finding']
        for inv in self:
            if inv.state not in ('draft', 'imported', 'matched'):
                raise UserError(_(
                    'Audit can only run on draft/imported/matched '
                    'invoices.'))
            inv.finding_ids.filtered(
                lambda f: f.status == 'open').unlink()
            contract = inv.contract_id
            pickings = self._match_pickings(inv)
            new_findings = []
            for line in inv.with_context(audit_running=True).line_ids:
                picking = pickings.get(line.tracking_ref or '')
                line.picking_id = picking.id if picking else False
                expected = 0.0
                if contract and line.charge_type == 'base_freight':
                    expected = contract.get_expected_amount(
                        'standard', 'standard', line.uom_weight,
                        '', '')
                elif contract and line.charge_type != 'base_freight':
                    base = sum(inv.line_ids.filtered(
                        lambda l: l.charge_type == 'base_freight'
                    ).mapped('amount_billed')) or 1.0
                    allowed = contract.allowed_surcharge_ids.filtered(
                        lambda s: s.charge_type == line.charge_type)
                    if not allowed:
                        new_findings.append({
                            'invoice_id': inv.id,
                            'invoice_line_id': line.id,
                            'finding_type': 'surcharge_unauthorized',
                            'severity': 'high',
                            'expected_amount': 0.0,
                            'actual_amount': line.amount_billed,
                        })
                        line.status = 'variance'
                        continue
                    expected = base * (allowed.max_pct / 100.0) \
                        if allowed.max_pct else line.amount_billed
                line.amount_expected = expected
                variance_pct = 0.0
                if expected:
                    variance_pct = abs(
                        line.amount_billed - expected) / expected * 100.0
                if line.charge_type == 'base_freight' and contract:
                    if variance_pct > contract.tolerance_pct:
                        sev = contract.severity_for_variance(variance_pct)
                        new_findings.append({
                            'invoice_id': inv.id,
                            'invoice_line_id': line.id,
                            'finding_type': 'rate_variance',
                            'severity': sev,
                            'expected_amount': expected,
                            'actual_amount': line.amount_billed,
                        })
                        line.status = 'variance'
                        continue
                if not picking and line.tracking_ref:
                    new_findings.append({
                        'invoice_id': inv.id,
                        'invoice_line_id': line.id,
                        'finding_type': 'phantom_shipment',
                        'severity': 'critical',
                        'expected_amount': 0.0,
                        'actual_amount': line.amount_billed,
                    })
                    line.status = 'variance'
                    continue
                line.status = 'matched'
            Finding.create(new_findings)
            duplicates = self._check_duplicates(inv)
            if duplicates:
                Finding.create([{
                    'invoice_id': inv.id,
                    'invoice_line_id': dup.id,
                    'finding_type': 'duplicate_billing',
                    'severity': 'critical',
                    'expected_amount': 0.0,
                    'actual_amount': dup.amount_billed,
                } for dup in duplicates])
            open_count = len(inv.finding_ids.filtered(
                lambda f: f.status == 'open'))
            if open_count:
                inv.state = 'discrepancy'
                critical = inv.finding_ids.filtered(
                    lambda f: f.severity == 'critical'
                    and f.status == 'open')
                if critical:
                    inv._notify_critical(critical)
            else:
                inv.state = 'matched'
        return True

    def _match_pickings(self, inv):
        """Batch-match tracking refs to stock.pickings (no N+1)."""
        refs = [r for r in inv.line_ids.mapped('tracking_ref') if r]
        if not refs:
            return {}
        pickings = self.env['stock.picking'].search([
            ('carrier_tracking_ref', 'in', refs),
        ])
        return {p.carrier_tracking_ref: p for p in pickings}

    def _check_duplicates(self, inv):
        dup_lines = self.env['sf.freight.invoice.line']
        for line in inv.line_ids.filtered(lambda l: l.tracking_ref):
            others = self.search([
                ('id', '!=', inv.id),
                ('carrier_id', '=', inv.carrier_id.id),
                ('state', 'not in', ('draft', 'cancelled')),
                ('line_ids.tracking_ref', '=', line.tracking_ref),
            ], limit=1)
            if others:
                dup_lines |= line
        return dup_lines

    def _notify_critical(self, findings):
        todo = self.env.ref('mail.mail_activity_data_todo',
                            raise_if_not_found=False)
        manager_group = self.env.ref(
            'sf_freight_audit.group_sf_freight_audit_manager',
            raise_if_not_found=False)
        users = manager_group.users if manager_group else self.env.user
        user = users[:1] or self.env.user
        existing = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', todo.id if todo else False),
            ('done', '=', False),
        ])
        if existing:
            return
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=user.id,
            summary=_('Critical freight audit findings'),
            note=_('%d critical finding(s) require review on %s.')
            % (len(findings), self.name),
            date_deadline=fields.Date.today() + __import__('datetime')
            .timedelta(days=2),
        )

    # ------------------------------------------------------------------
    # Workflow actions
    # ------------------------------------------------------------------
    def action_validate_payment(self):
        for inv in self:
            open_disputes = inv.dispute_ids.filtered(
                lambda d: d.state not in ('resolved', 'closed'))
            if open_disputes:
                raise UserError(_(
                    '%d open dispute(s) block payment on %s.')
                    % (len(open_disputes), inv.name))
            if inv.open_finding_count:
                raise UserError(_(
                    '%d open finding(s) block payment on %s.')
                    % (inv.open_finding_count, inv.name))
            if inv.state != 'validated':
                raise UserError(_('Invoice must be validated first.'))
            inv.state = 'paid'

    def action_mark_validated(self):
        for inv in self:
            if inv.open_finding_count:
                raise UserError(_(
                    'Resolve open findings before validation.'))
            if inv.state not in ('matched', 'discrepancy'):
                raise UserError(_('Cannot validate from this state.'))
            inv.state = 'validated'

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfFreightInvoiceLine(models.Model):
    _name = 'sf.freight.invoice.line'
    _description = 'Freight Invoice Line'
    _order = 'id'

    invoice_id = fields.Many2one('sf.freight.invoice', string='Invoice',
                                 required=True, ondelete='cascade',
                                 index=True)
    description = fields.Char(string='Description')
    charge_type = fields.Selection(CHARGE_TYPES, string='Charge Type',
                                   required=True, default='base_freight')
    tracking_ref = fields.Char(string='Tracking Reference', index=True)
    ship_date = fields.Date(string='Shipment Date')
    qty = fields.Float(string='Quantity', default=1.0)
    uom_weight = fields.Float(string='Weight (kg)')
    amount_billed = fields.Monetary(string='Amount Billed',
                                    currency_field='currency_id')
    amount_expected = fields.Monetary(string='Amount Expected',
                                      currency_field='currency_id')
    variance = fields.Monetary(
        string='Variance', currency_field='currency_id',
        compute='_compute_variance', store=True)
    currency_id = fields.Many2one(related='invoice_id.currency_id')
    picking_id = fields.Many2one('stock.picking', string='Matched Shipment',
                                 ondelete='set null', readonly=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('variance', 'Variance'),
        ('disputed', 'Disputed'),
        ('excluded', 'Excluded'),
    ], string='Status', default='pending', index=True)

    @api.depends('amount_billed', 'amount_expected')
    def _compute_variance(self):
        for line in self:
            line.variance = line.amount_billed - line.amount_expected

    @api.constrains('status')
    def _check_excluded_note(self):
        for line in self:
            if line.status == 'excluded':
                has_finding = bool(self.env['sf.freight.finding'].search([
                    ('invoice_line_id', '=', line.id)], limit=1))
                if not has_finding and not line.description:
                    raise UserError(_(
                        'An excluded line requires an explanation in the '
                        'description field.'))
