# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FuelVehicle(models.Model):
    _name = 'sf.fuel.vehicle'
    _description = 'Fuel Vehicle'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    license_plate = fields.Char(string='License plate', index=True)
    brand = fields.Char(string='Brand')
    model = fields.Char(string='Model')
    fuel_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('gasoline', 'Gasoline'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
        ('other', 'Other'),
    ], string='Fuel type', default='diesel', required=True)
    card_id = fields.Many2one('sf.fuel.card', string='Fuel card',
                              ondelete='restrict')
    fill_ids = fields.One2many('sf.fuel.fill', 'vehicle_id',
                               string='Fills')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('license_plate_uniq', 'UNIQUE(license_plate)',
         _('This license plate is already in use.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.fuel.vehicle')
            vals['name'] = seq
        return super().create(vals)


class FuelCard(models.Model):
    _name = 'sf.fuel.card'
    _description = 'Fuel Card'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    card_number = fields.Char(string='Card number', index=True)
    vehicle_id = fields.Many2one('sf.fuel.vehicle', string='Vehicle',
                                 ondelete='restrict')
    limit_amount = fields.Float(string='Monthly limit', default=0.0)
    state = fields.Selection([
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
    ], string='Status', default='active', required=True, tracking=True,
       index=True)
    expiry_date = fields.Date(string='Expiry date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('card_number_uniq', 'UNIQUE(card_number)',
         _('This card number is already in use.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.fuel.card')
            vals['name'] = seq
        return super().create(vals)

    def action_block(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_fuel_management.group_fuel_manager'):
            raise UserError(_('Only a fuel manager can block a card.'))
        self.state = 'blocked'

    def action_expire(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_fuel_management.group_fuel_manager'):
            raise UserError(_('Only a fuel manager can expire a card.'))
        self.state = 'expired'

    def action_activate(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_fuel_management.group_fuel_manager'):
            raise UserError(_('Only a fuel manager can activate a card.'))
        self.state = 'active'


class FuelFill(models.Model):
    _name = 'sf.fuel.fill'
    _description = 'Fuel Fill'
    _order = 'vehicle_id, odometer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    vehicle_id = fields.Many2one('sf.fuel.vehicle', string='Vehicle',
                                 required=True, ondelete='restrict',
                                 index=True)
    card_id = fields.Many2one('sf.fuel.card', string='Fuel card',
                              ondelete='restrict')
    fill_date = fields.Date(string='Fill date', required=True,
                            default=fields.Date.context_today, index=True)
    odometer = fields.Float(string='Odometer (km)', required=True)
    liters = fields.Float(string='Liters', required=True)
    price_per_liter = fields.Float(string='Price per liter', required=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    consumption = fields.Float(string='Consumption (L/100km)',
                               compute='_compute_consumption', store=True)
    previous_odometer = fields.Float(string='Previous odometer (km)',
                                     compute='_compute_consumption',
                                     store=True)
    supplier = fields.Char(string='Supplier')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('recorded', 'Recorded'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This fill number already exists.')),
    ]

    @api.depends('liters', 'price_per_liter')
    def _compute_total(self):
        for fill in self:
            fill.total = fill.liters * fill.price_per_liter

    @api.depends('vehicle_id', 'odometer', 'liters')
    def _compute_consumption(self):
        for fill in self:
            previous = self.search([
                ('vehicle_id', '=', fill.vehicle_id.id),
                ('odometer', '<', fill.odometer),
                ('id', '!=', fill.id),
            ], order='odometer desc', limit=1)
            fill.previous_odometer = previous.odometer if previous else 0.0
            if not previous or not previous.odometer:
                fill.consumption = 0.0
            else:
                diff = fill.odometer - previous.odometer
                fill.consumption = (fill.liters / diff) * 100 if diff > 0 \
                    else 0.0

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.fuel.fill')
        fill = super().create(vals)
        fill._check_card()
        return fill

    def write(self, vals):
        res = super().write(vals)
        self._check_card()
        return res

    def _check_card(self):
        for fill in self:
            if fill.card_id and fill.card_id.state in ('blocked', 'expired'):
                raise UserError(_('Card %s is blocked or expired and cannot '
                                  'be used.') % fill.card_id.name)

    def action_record(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft fills can be recorded.'))
        if not self.env.user.has_group('sf_fuel_management.group_fuel_manager'):
            raise UserError(_('Only a fuel manager can record a fill.'))
        self.state = 'recorded'

    def action_done(self):
        self.ensure_one()
        if self.state != 'recorded':
            raise UserError(_('Only recorded fills can be marked as done.'))
        self.state = 'done'

    @api.model
    def _check_fuel_alerts(self):
        todo = self.env.ref('mail.mail_activity_data_todo')
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            cards = self.env['sf.fuel.card'].with_company(company).search([
                ('state', '!=', 'expired'),
                ('expiry_date', '!=', False),
                ('company_id', '=', company.id),
            ])
            for card in cards:
                if card.expiry_date - timedelta(
                        days=company.sf_fuel_alert_days) > today:
                    continue
                existing = card.activity_ids.filtered(
                    lambda a: a.activity_type_id == todo and a.state != 'done')
                if existing:
                    continue
                card.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Fuel card %s expires soon') % card.name,
                    user_id=self.env.user.id)
            abnormal = self.with_company(company).search([
                ('consumption', '>', company.sf_fuel_max_l100),
                ('company_id', '=', company.id),
            ])
            for fill in abnormal:
                existing = fill.activity_ids.filtered(
                    lambda a: a.activity_type_id == todo and a.state != 'done')
                if existing:
                    continue
                fill.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Abnormal fuel consumption: %s') % fill.name,
                    user_id=self.env.user.id)


class FuelTank(models.Model):
    _name = 'sf.fuel.tank'
    _description = 'Fuel Tank'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    site = fields.Char(string='Site', required=True)
    fuel_type = fields.Selection([
        ('diesel', 'Diesel'),
        ('gasoline', 'Gasoline'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
        ('other', 'Other'),
    ], string='Fuel type', default='diesel', required=True)
    capacity = fields.Float(string='Capacity (liters)', required=True)
    current_level = fields.Float(string='Current level (liters)', default=0.0)
    last_gauge_date = fields.Date(string='Last gauge date')
    receipt_ids = fields.One2many('sf.fuel.tank.receipt', 'tank_id',
                                  string='Receipts')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.fuel.tank')
            vals['name'] = seq
        return super().create(vals)


class FuelTankReceipt(models.Model):
    _name = 'sf.fuel.tank.receipt'
    _description = 'Fuel Tank Receipt'
    _order = 'receipt_date desc'

    name = fields.Char(string='Number', required=True, index=True)
    tank_id = fields.Many2one('sf.fuel.tank', string='Tank', required=True,
                              ondelete='restrict', index=True)
    receipt_date = fields.Date(string='Receipt date', required=True,
                               default=fields.Date.context_today, index=True)
    liters = fields.Float(string='Liters', required=True)
    supplier = fields.Char(string='Supplier')
    unit_price = fields.Float(string='Unit price', required=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('liters', 'unit_price')
    def _compute_total(self):
        for receipt in self:
            receipt.total = receipt.liters * receipt.unit_price

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.fuel.tank.receipt')
            vals['name'] = seq
        return super().create(vals)