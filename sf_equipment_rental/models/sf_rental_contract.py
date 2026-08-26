# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfRentalContract(models.Model):
    _name = 'sf.rental.contract'
    _description = 'Rental Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rental.activity.mixin']
    _order = 'start_datetime desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    start_datetime = fields.Datetime(string='Start', required=True)
    end_datetime = fields.Datetime(string='End', required=True)
    line_ids = fields.One2many('sf.rental.contract.line', 'contract_id', string='Lines')
    amount_total = fields.Monetary(string='Total', compute='_compute_amount_total', store=True, currency_field='currency_id')
    penalty_total = fields.Monetary(string='Penalties', compute='_compute_penalty_total', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('invoiced', 'Invoiced'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    inspection_out_ids = fields.One2many('sf.rental.inspection', 'contract_id', string='Out Inspections', domain=[('direction', '=', 'out')])
    inspection_in_ids = fields.One2many('sf.rental.inspection', 'contract_id', string='In Inspections', domain=[('direction', '=', 'in')])
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='set null')
    amount_due = fields.Monetary(string='Amount Due', compute='_compute_amount_due', store=True, currency_field='currency_id')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for contract in self:
            contract.amount_total = sum(contract.line_ids.mapped('subtotal'))

    @api.depends('inspection_in_ids.damage_ids.penalty_amount')
    def _compute_penalty_total(self):
        for contract in self:
            contract.penalty_total = sum(
                damage.penalty_amount for inspection in contract.inspection_in_ids for damage in inspection.damage_ids
            )

    @api.depends('amount_total', 'penalty_total')
    def _compute_amount_due(self):
        for contract in self:
            contract.amount_due = contract.amount_total + contract.penalty_total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.contract')
            if vals.get('state', 'draft') != 'draft':
                raise UserError(_('Contracts can only be created in draft.'))
        return super().create(vals_list)

    _STATE_FLOW = {
        'draft': ('confirmed', 'cancelled'),
        'confirmed': ('active', 'cancelled'),
        'active': ('returned',),
        'returned': ('invoiced', 'cancelled'),
        'invoiced': ('closed',),
        'closed': (),
        'cancelled': (),
    }

    def write(self, vals):
        for record in self:
            if 'state' in vals and vals['state'] != record.state:
                allowed = self._STATE_FLOW.get(record.state, ())
                if vals['state'] not in allowed:
                    raise UserError(_('Invalid status transition %s -> %s.') % (record.state, vals['state']))
            if record.state not in ('draft', 'cancelled') and any(
                f in vals for f in ('start_datetime', 'end_datetime', 'line_ids', 'partner_id')
            ):
                raise UserError(_('A %s contract cannot be edited.') % record.state)
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_equipment_rental.group_sf_rental_manager'):
            raise UserError(_('Only a rental manager can perform this action.'))

    def _check_conflict(self, equipment_id, start, end, exclude_line_id=None):
        domain = [
            ('equipment_id', '=', equipment_id),
            ('contract_id.state', 'in', ('confirmed', 'active')),
        ]
        if exclude_line_id:
            domain.append(('id', '!=', exclude_line_id))
        conflicts = self.env['sf.rental.contract.line'].search(domain).filtered(
            lambda l: l.contract_id.start_datetime < end and l.contract_id.end_datetime > start
        )
        if conflicts:
            raise UserError(_('The equipment is already rented during this period.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft contracts can be confirmed.'))
        if self.end_datetime <= self.start_datetime:
            raise UserError(_('The end date must be after the start date.'))
        if not self.line_ids:
            raise UserError(_('The contract has no equipment lines.'))
        for line in self.line_ids:
            self._check_conflict(line.equipment_id.id, self.start_datetime, self.end_datetime, exclude_line_id=line.id)
        self.state = 'confirmed'

    def action_active(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed contracts can be activated.'))
        for line in self.line_ids:
            equipment = line.equipment_id
            if equipment.state == 'maintenance':
                raise UserError(_('Equipment %s is under maintenance and cannot be rented.') % equipment.name)
            if equipment.state == 'retired':
                raise UserError(_('Equipment %s is retired and cannot be rented.') % equipment.name)
            equipment.state = 'out'
            self.env['sf.rental.inspection'].create({
                'contract_id': self.id,
                'line_id': line.id,
                'direction': 'out',
            })
        self.state = 'active'

    def action_return(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active contracts can be returned.'))
        missing = self.line_ids.filtered(
            lambda l: not self.inspection_in_ids.filtered(
                lambda i: i.line_id.id == l.id and i.state == 'done'
            )
        )
        if missing:
            raise UserError(_('Every equipment line requires a completed in inspection before return.'))
        self.state = 'returned'
        for line in self.line_ids:
            line.equipment_id.state = 'available'

    def action_invoice(self):
        self.ensure_one()
        if self.state != 'returned':
            raise UserError(_('Only returned contracts can be invoiced.'))
        if not self.invoice_id:
            income_account = self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', self.company_id.id),
            ], limit=1)
            penalty_account_id = self.env['ir.config_parameter'].sudo().get_param(
                'sf_equipment_rental.penalty_account_id')
            penalty_account = self.env['account.account'].browse(
                int(penalty_account_id)) if penalty_account_id else income_account
            journal = self.env['account.journal'].search([
                ('company_id', '=', self.company_id.id),
                ('type', '=', 'sale'),
            ], limit=1)
            if not income_account or not journal:
                raise UserError(_('Configure an income account and a sale journal for the company before invoicing.'))
            lines = [(0, 0, {
                'name': self.name,
                'quantity': 1,
                'price_unit': self.amount_total,
                'account_id': income_account.id,
            })]
            if self.penalty_total:
                lines.append((0, 0, {
                    'name': '%s - Penalties' % self.name,
                    'quantity': 1,
                    'price_unit': self.penalty_total,
                    'account_id': penalty_account.id if penalty_account else income_account.id,
                }))
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_date': fields.Date.context_today(self),
                'journal_id': journal.id,
                'invoice_line_ids': lines,
            })
            invoice.action_post()
            self.invoice_id = invoice.id
        self.state = 'invoiced'

    def action_close(self):
        self.ensure_one()
        if self.state != 'invoiced':
            raise UserError(_('Only invoiced contracts can be closed.'))
        if not self.invoice_id or self.invoice_id.state != 'posted':
            raise UserError(_('The contract can only be closed once the invoice is posted.'))
        self.state = 'closed'

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('active', 'returned', 'invoiced', 'closed'):
            raise UserError(_('A %s contract cannot be cancelled.') % self.state)
        if self.state == 'confirmed':
            self._check_manager()
        self.state = 'cancelled'