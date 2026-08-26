# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfFreightCarrierContract(models.Model):
    _name = 'sf.freight.carrier.contract'
    _description = 'Freight Carrier Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Carrier',
                                 required=True, ondelete='restrict',
                                 domain=[('is_company', '=', True)])
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    tolerance_pct = fields.Float(string='Rate Tolerance %', default=0.5,
                                 help='Accepted variance between billed and '
                                      'expected amount, in percent.')
    warn_pct = fields.Float(string='Medium Severity %', default=2.0)
    high_pct = fields.Float(string='High Severity %', default=5.0)
    crit_pct = fields.Float(string='Critical Severity %', default=10.0)
    date_start = fields.Date(string='Start Date', required=True,
                             default=fields.Date.today)
    date_end = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True, copy=False)
    rate_line_ids = fields.One2many('sf.freight.rate.line', 'contract_id',
                                    string='Rate Grid')
    allowed_surcharge_ids = fields.One2many(
        'sf.freight.surcharge.allowed', 'contract_id',
        string='Allowed Surcharges')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.freight.carrier.contract') or _('New')
            if vals.get('state', 'draft') not in ('draft', 'active'):
                raise UserError(_('Contracts can only be created as draft or active.'))
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals:
            for rec in self:
                allowed = {'draft': {'draft', 'active', 'archived'},
                           'active': {'active', 'expired', 'archived'},
                           'expired': {'expired', 'archived'},
                           'archived': {'archived'}}
                if vals['state'] not in allowed.get(rec.state, set()):
                    raise UserError(_(
                        'Invalid contract transition %s -> %s.')
                        % (rec.state, vals['state']))
        return super().write(vals)

    def unlink(self):
        if any(rec.state not in ('draft', 'archived') for rec in self):
            raise UserError(_('Only draft or archived contracts can be deleted.'))
        return super().unlink()

    def action_activate(self):
        for rec in self:
            overlap = self.search([
                ('id', '!=', rec.id),
                ('partner_id', '=', rec.partner_id.id),
                ('state', '=', 'active'),
                ('company_id', '=', rec.company_id.id),
            ])
            if overlap:
                raise UserError(_(
                    'An active contract already exists for this carrier.'))
            rec.state = 'active'

    def action_archive(self):
        self.write({'state': 'archived'})

    def get_expected_amount(self, charge_type, service_level, weight,
                            zone_from, zone_to):
        """Return expected base price from the grid (linear weight bands)."""
        self.ensure_one()
        line = self.rate_line_ids.filtered(lambda l: (
            l.service_level == service_level
            and l.weight_from <= weight
            and (not l.weight_to or weight <= l.weight_to)
            and (not l.zone_from or l.zone_from == zone_from)
            and (not l.zone_to or l.zone_to == zone_to)
        ))[:1]
        if not line:
            return 0.0
        amount = line.base_price + line.price_per_kg * max(
            0.0, weight - (line.weight_from or 0.0))
        return max(amount, line.min_charge or 0.0)

    def severity_for_variance(self, pct):
        self.ensure_one()
        if pct > self.crit_pct:
            return 'critical'
        if pct > self.high_pct:
            return 'high'
        if pct > self.warn_pct:
            return 'medium'
        return 'low'


class SfFreightRateLine(models.Model):
    _name = 'sf.freight.rate.line'
    _description = 'Freight Contract Rate Line'
    _order = 'weight_from, id'

    contract_id = fields.Many2one('sf.freight.carrier.contract',
                                  string='Contract', required=True,
                                  ondelete='cascade', index=True)
    service_level = fields.Selection([
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('economy', 'Economy'),
        ('ltl', 'LTL'),
        ('ftl', 'FTL'),
    ], string='Service Level', required=True, default='standard')
    zone_from = fields.Char(string='Zone From')
    zone_to = fields.Char(string='Zone To')
    weight_from = fields.Float(string='Weight From (kg)', default=0.0)
    weight_to = fields.Float(string='Weight To (kg)')
    base_price = fields.Monetary(string='Base Price', currency_field='currency_id')
    price_per_kg = fields.Monetary(string='Price per Extra kg',
                                   currency_field='currency_id')
    min_charge = fields.Monetary(string='Minimum Charge',
                                 currency_field='currency_id')
    currency_id = fields.Many2one(related='contract_id.currency_id')

    _sql_constraints = [
        ('sf_rate_weight_check',
         'CHECK(weight_to = 0 OR weight_to > weight_from)',
         'Weight To must be greater than Weight From.'),
        ('sf_rate_price_check',
         'CHECK(base_price >= 0 AND price_per_kg >= 0 AND min_charge >= 0)',
         'Prices cannot be negative.'),
    ]


class SfFreightSurchargeAllowed(models.Model):
    _name = 'sf.freight.surcharge.allowed'
    _description = 'Allowed Surcharge per Contract'

    contract_id = fields.Many2one('sf.freight.carrier.contract',
                                  string='Contract', required=True,
                                  ondelete='cascade', index=True)
    charge_type = fields.Selection([
        ('fuel_surcharge', 'Fuel Surcharge'),
        ('security', 'Security Fee'),
        ('residential', 'Residential Delivery'),
        ('liftgate', 'Liftgate'),
        ('insurance', 'Insurance'),
        ('customs', 'Customs Handling'),
        ('accessorial_other', 'Other Accessorial'),
    ], string='Charge Type', required=True)
    max_pct = fields.Float(string='Max % of Base', default=0.0,
                           help='Maximum percentage of the base freight '
                                'amount. 0 = unlimited.')

    _sql_constraints = [
        ('sf_surcharge_uniq', 'unique(contract_id, charge_type)',
         'Each surcharge type can only be listed once per contract.'),
    ]
