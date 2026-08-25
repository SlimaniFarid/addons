# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityTariff(models.Model):
    _name = 'sf.utility.tariff'
    _description = 'Utility Tariff'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.utility.activity.mixin']
    _order = 'effective_from desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    utility_type = fields.Selection([
        ('water', 'Water'),
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('heating', 'Heating'),
        ('other', 'Other'),
    ], string='Utility Type', required=True, default='water')
    effective_from = fields.Date(string='Effective From', required=True)
    line_ids = fields.One2many('sf.utility.tariff.line', 'tariff_id', string='Tiers')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def _check_manager(self):
        if not self.env.user.has_group('sf_utility_billing.group_sf_utility_manager'):
            raise UserError(_('Only a utility manager can perform this action.'))

    @api.model_create_multi
    def create(self, vals_list):
        self._check_manager()
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.utility.tariff')
        tariffs = super().create(vals_list)
        tariffs._check_lines()
        return tariffs

    def write(self, vals):
        self._check_manager()
        res = super().write(vals)
        self._check_lines()
        return res

    def _check_lines(self):
        for tariff in self:
            lines = tariff.line_ids.sorted(key=lambda l: l.from_quantity)
            for i, line in enumerate(lines):
                if line.to_quantity and line.to_quantity <= line.from_quantity:
                    raise UserError(_('The "To Quantity" must be greater than the "From Quantity".'))
                if i == 0:
                    continue
                previous = lines[i - 1]
                if not previous.to_quantity:
                    raise UserError(_('No tier may follow a tier without an upper limit.'))
                if line.from_quantity < previous.to_quantity:
                    raise UserError(_('Tariff tiers must not overlap.'))
                if line.from_quantity > previous.to_quantity:
                    raise UserError(_('Tariff tiers must be contiguous.'))


class SfUtilityTariffLine(models.Model):
    _name = 'sf.utility.tariff.line'
    _description = 'Utility Tariff Tier'
    _order = 'from_quantity asc, id asc'

    tariff_id = fields.Many2one('sf.utility.tariff', string='Tariff', required=True, ondelete='cascade')
    from_quantity = fields.Float(string='From Quantity', required=True)
    to_quantity = fields.Float(string='To Quantity', help='Leave empty for an unlimited tier.')
    price_per_unit = fields.Monetary(string='Price per Unit', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.constrains('from_quantity', 'to_quantity')
    def _check_quantities(self):
        for line in self:
            if line.to_quantity and line.to_quantity <= line.from_quantity:
                raise UserError(_('The "To Quantity" must be greater than the "From Quantity".'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tariff_id') and not vals.get('company_id'):
                tariff = self.env['sf.utility.tariff'].browse(vals['tariff_id'])
                vals['company_id'] = tariff.company_id.id
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.utility.activity.mixin'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

