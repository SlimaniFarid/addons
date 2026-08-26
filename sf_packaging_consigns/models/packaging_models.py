# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PackagingType(models.Model):
    _name = 'sf.packaging.type'
    _description = 'Deposit Packaging Type'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    product_name = fields.Char(string='Product name')
    condition = fields.Integer(string='Units per lot')
    deposit_amount = fields.Float(string='Deposit amount', default=0.0)
    min_stock = fields.Integer(string='Minimum stock', default=0)
    park_ids = fields.One2many('sf.packaging.park', 'packaging_type_id',
                               string='Parks')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.packaging.type')
        return super().create(vals)


class PackagingSite(models.Model):
    _name = 'sf.packaging.site'
    _description = 'Packaging Site'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    address = fields.Char(string='Address')
    manager_id = fields.Many2one('res.users', string='Site manager',
                                 ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.packaging.site')
        return super().create(vals)


class PackagingPark(models.Model):
    _name = 'sf.packaging.park'
    _description = 'Packaging Park'
    _order = 'packaging_type_id, site_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    packaging_type_id = fields.Many2one('sf.packaging.type',
                                        string='Packaging type',
                                        required=True, ondelete='cascade',
                                        index=True)
    site_id = fields.Many2one('sf.packaging.site', string='Site',
                              required=True, ondelete='cascade',
                              index=True)
    quantity = fields.Integer(string='Quantity', default=0)
    move_done_qty = fields.Integer(string='Emissions done',
                                   compute='_compute_balance', store=True)
    return_received_qty = fields.Integer(string='Returns received',
                                         compute='_compute_balance',
                                         store=True)
    available_quantity = fields.Integer(string='Available quantity',
                                        compute='_compute_balance',
                                        store=True)
    return_rate = fields.Float(string='Return rate (%)',
                               compute='_compute_balance', store=True)
    low_stock = fields.Boolean(string='Low stock',
                               compute='_compute_low_stock', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('type_site_uniq', 'UNIQUE(packaging_type_id, site_id)',
         _('A park already exists for this packaging type and site.')),
    ]

    @api.depends('packaging_type_id', 'site_id')
    def _compute_balance(self):
        for park in self:
            moves = self.env['sf.packaging.move'].search([
                ('packaging_type_id', '=', park.packaging_type_id.id),
                ('site_id', '=', park.site_id.id),
                ('company_id', '=', park.company_id.id),
                ('state', 'in', ['done', 'closed']),
            ])
            returns = self.env['sf.packaging.return'].search([
                ('packaging_type_id', '=', park.packaging_type_id.id),
                ('site_id', '=', park.site_id.id),
                ('company_id', '=', park.company_id.id),
                ('state', 'in', ['received', 'checked']),
            ])
            park.move_done_qty = sum(moves.mapped('quantity') or [0])
            park.return_received_qty = sum(returns.mapped('quantity') or [0])
            park.available_quantity = park.move_done_qty \
                - park.return_received_qty
            park.return_rate = park.move_done_qty and (
                park.return_received_qty * 100.0 / park.move_done_qty) \
                or 0.0

    @api.depends('available_quantity', 'packaging_type_id.min_stock')
    def _compute_low_stock(self):
        for park in self:
            park.low_stock = park.available_quantity < \
                park.packaging_type_id.min_stock

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.packaging.park')
        return super().create(vals)

    def _check_packaging_alerts(self):
        companies = self.env['res.company'].search([])
        manager = self.env.ref(
            'sf_packaging_consigns.group_packaging_manager')
        user = manager.users[:1] if manager.users else self.env.user
        for company in companies:
            parks = self.with_company(company).search([
                ('company_id', '=', company.id),
            ])
            for park in parks:
                if park.available_quantity >= \
                        park.packaging_type_id.min_stock:
                    continue
                existing = park.activity_ids.filtered(
                    lambda a: a.activity_type_id ==
                    self.env.ref('mail.mail_activity_data_todo')
                    and a.state != 'done')
                if existing:
                    continue
                park.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Park under minimum stock: %s')
                    % (park.name,),
                    user_id=user.id)


class PackagingMove(models.Model):
    _name = 'sf.packaging.move'
    _description = 'Packaging Emission'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    packaging_type_id = fields.Many2one('sf.packaging.type',
                                        string='Packaging type',
                                        required=True, ondelete='restrict',
                                        index=True)
    site_id = fields.Many2one('sf.packaging.site', string='Site',
                              required=True, ondelete='restrict',
                              index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True, ondelete='restrict',
                                 index=True)
    quantity = fields.Integer(string='Quantity', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,
                       required=True, index=True)
    reference = fields.Char(string='Reference')
    deposit_total = fields.Float(string='Deposit total',
                                 compute='_compute_deposit_total',
                                 store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)',
         _('The quantity must be positive.')),
    ]

    @api.depends('quantity', 'packaging_type_id.deposit_amount')
    def _compute_deposit_total(self):
        for move in self:
            move.deposit_total = (move.quantity or 0) * (
                move.packaging_type_id.deposit_amount or 0.0)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.packaging.move')
        return super().create(vals)

    def action_done(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft moves can be marked as done.'))
        if not self.env.user.has_group(
                'sf_packaging_consigns.group_packaging_manager'):
            raise UserError(_('Only packaging managers can validate '
                              'moves.'))
        self.state = 'done'
        park = self.env['sf.packaging.park'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('site_id', '=', self.site_id.id),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if park:
            park.quantity += self.quantity
        else:
            park = self.env['sf.packaging.park'].create({
                'packaging_type_id': self.packaging_type_id.id,
                'site_id': self.site_id.id,
                'quantity': self.quantity,
                'company_id': self.company_id.id,
            })
        park._compute_balance()

    def action_close(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only done moves can be closed.'))
        if not self.env.user.has_group(
                'sf_packaging_consigns.group_packaging_manager'):
            raise UserError(_('Only packaging managers can close moves.'))
        self.state = 'closed'
        park = self.env['sf.packaging.park'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('site_id', '=', self.site_id.id),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if park:
            park._compute_balance()


class PackagingReturn(models.Model):
    _name = 'sf.packaging.return'
    _description = 'Packaging Return'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    packaging_type_id = fields.Many2one('sf.packaging.type',
                                        string='Packaging type',
                                        required=True, ondelete='restrict',
                                        index=True)
    site_id = fields.Many2one('sf.packaging.site', string='Site',
                              required=True, ondelete='restrict',
                              index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True, ondelete='restrict',
                                 index=True)
    quantity = fields.Integer(string='Quantity', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,
                       required=True, index=True)
    received_ok = fields.Integer(string='Received OK')
    deposit_total = fields.Float(string='Deposit total',
                                 compute='_compute_deposit_total',
                                 store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('checked', 'Checked'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)',
         _('The quantity must be positive.')),
    ]

    @api.depends('quantity', 'packaging_type_id.deposit_amount')
    def _compute_deposit_total(self):
        for ret in self:
            ret.deposit_total = (ret.quantity or 0) * (
                ret.packaging_type_id.deposit_amount or 0.0)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.packaging.return')
        return super().create(vals)

    def _partner_outstanding(self):
        self.ensure_one()
        issued = self.env['sf.packaging.move'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('partner_id', '=', self.partner_id.id),
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ['done', 'closed']),
        ])
        received = self.env['sf.packaging.return'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('partner_id', '=', self.partner_id.id),
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ['received', 'checked']),
        ])
        issued_qty = sum(issued.mapped('quantity') or [0])
        received_qty = sum(received.mapped('quantity') or [0])
        return issued_qty - received_qty

    def action_received(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft returns can be marked as '
                              'received.'))
        outstanding = self._partner_outstanding()
        if self.quantity > outstanding:
            raise UserError(_('The return cannot exceed the outstanding '
                              'consigned balance of the partner (%s).')
                            % outstanding)
        self.state = 'received'
        park = self.env['sf.packaging.park'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('site_id', '=', self.site_id.id),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if park:
            park.quantity = max(0, park.quantity - self.quantity)
            park._compute_balance()

    def action_checked(self):
        self.ensure_one()
        if self.state != 'received':
            raise UserError(_('Only received returns can be checked.'))
        if not self.env.user.has_group(
                'sf_packaging_consigns.group_packaging_manager'):
            raise UserError(_('Only packaging managers can check '
                              'returns.'))
        self.state = 'checked'
        park = self.env['sf.packaging.park'].search([
            ('packaging_type_id', '=', self.packaging_type_id.id),
            ('site_id', '=', self.site_id.id),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if park:
            park._compute_balance()