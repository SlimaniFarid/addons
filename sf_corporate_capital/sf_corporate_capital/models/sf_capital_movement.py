# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfCapitalMovement(models.Model):
    _name = 'sf.capital.movement'
    _description = 'Capital Movement'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.capital.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    shareholder_id = fields.Many2one(
        'sf.shareholder', string='Shareholder', ondelete='cascade')
    from_shareholder_id = fields.Many2one(
        'sf.shareholder', string='From Shareholder', ondelete='cascade')
    to_shareholder_id = fields.Many2one(
        'sf.shareholder', string='To Shareholder', ondelete='cascade')
    share_class_id = fields.Many2one(
        'sf.share.class', string='Share Class', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    unit_price = fields.Monetary(
        string='Unit Price', currency_field='currency_id')
    amount = fields.Monetary(
        string='Amount', compute='_compute_amount', store=True,
        currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    movement_type = fields.Selection([
        ('issue', 'Issue'),
        ('transfer', 'Transfer'),
        ('buyback', 'Buyback'),
    ], string='Movement Type', default='issue', required=True)
    date = fields.Date(string='Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('capital_movement_positive_quantity',
         'CHECK (quantity > 0)',
         'The quantity must be strictly positive.'),
        ('capital_movement_transfer_distinct_shareholders',
         'CHECK (movement_type != \'transfer\' OR from_shareholder_id != to_shareholder_id)',
         'For transfers, from and to shareholders must be different.'),
    ]

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for move in self:
            move.amount = move.quantity * (move.unit_price or 0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.capital.movement')
            if vals.get('shareholder_id') and not vals.get('company_id'):
                shareholder = self.env['sf.shareholder'].browse(
                    vals['shareholder_id'])
                vals['company_id'] = shareholder.company_id.id
            elif vals.get('from_shareholder_id') and not vals.get('company_id'):
                shareholder = self.env['sf.shareholder'].browse(
                    vals['from_shareholder_id'])
                vals['company_id'] = shareholder.company_id.id
            elif vals.get('to_shareholder_id') and not vals.get('company_id'):
                shareholder = self.env['sf.shareholder'].browse(
                    vals['to_shareholder_id'])
                vals['company_id'] = shareholder.company_id.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_corporate_capital.group_sf_capital_manager'):
            raise UserError(_('Only a capital manager can perform this action.'))

    def _set_state(self, state):
        self.with_context(sf_capital_bypass_state=True).write(
            {'state': state})

    def write(self, vals):
        if 'state' in vals and not self.env.context.get(
                'sf_capital_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        posted = self.filtered(lambda m: m.state == 'posted')
        if posted and not self.env.context.get('sf_capital_bypass_state'):
            raise UserError(_('A posted capital movement cannot be modified.'))
        return super().write(vals)

    @api.constrains('movement_type', 'shareholder_id', 'from_shareholder_id', 'to_shareholder_id')
    def _check_shareholder_requirements(self):
        for move in self:
            if move.movement_type in ('issue', 'buyback'):
                if not move.shareholder_id:
                    raise ValidationError(_(
                        'Shareholder is required for issue and buyback movements.'))
                if move.from_shareholder_id or move.to_shareholder_id:
                    raise ValidationError(_(
                        'From/To shareholders are not allowed for issue and buyback movements.'))
            elif move.movement_type == 'transfer':
                if not move.from_shareholder_id or not move.to_shareholder_id:
                    raise ValidationError(_(
                        'From and To shareholders are required for transfer movements.'))
                if move.shareholder_id:
                    raise ValidationError(_(
                        'Shareholder field is not used for transfer movements.'))

    def _held_quantity(self, shareholder, share_class, movement_type='sell'):
        """Compute held quantity for a shareholder in a share class.
        
        For sell/buyback: quantities the shareholder currently holds.
        For transfer (from): quantities the from_shareholder holds.
        """
        moves = self.env['sf.capital.movement'].search([
            ('share_class_id', '=', share_class.id),
            ('state', '=', 'posted'),
            ('id', '!=', self.id),
        ])
        held = 0
        for move in moves:
            if move.movement_type == 'issue':
                if move.shareholder_id == shareholder:
                    held += move.quantity
            elif move.movement_type == 'buyback':
                if move.shareholder_id == shareholder:
                    held -= move.quantity
            elif move.movement_type == 'transfer':
                if move.from_shareholder_id == shareholder:
                    held -= move.quantity
                if move.to_shareholder_id == shareholder:
                    held += move.quantity
        return held

    def action_post(self):
        for record in self:
            record._check_manager()
            if record.state != 'draft':
                raise UserError(_('Only draft capital movements can be posted.'))
            if record.movement_type == 'buyback':
                held = record._held_quantity(
                    record.shareholder_id, record.share_class_id)
                if held < record.quantity:
                    raise ValidationError(_(
                        'The shareholder does not hold enough shares of this '
                        'class to buyback %s shares (held: %s).') % (
                            record.quantity, held))
            elif record.movement_type == 'transfer':
                held = record._held_quantity(
                    record.from_shareholder_id, record.share_class_id)
                if held < record.quantity:
                    raise ValidationError(_(
                        'The from shareholder does not hold enough shares of this '
                        'class to transfer %s shares (held: %s).') % (
                            record.quantity, held))
            record._set_state('posted')

    def action_cancel(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('A cancelled capital movement cannot be cancelled.'))
            if record.state == 'posted':
                record._check_manager()
            record._set_state('cancelled')