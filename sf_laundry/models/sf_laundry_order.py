# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfLaundryOrder(models.Model):
    _name = 'sf.laundry.order'
    _description = 'Laundry Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.laundry.activity.mixin']
    _order = 'deposit_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='set null')
    customer_name = fields.Char(string='Customer Name')
    phone = fields.Char(string='Phone')
    deposit_date = fields.Date(string='Deposit Date', default=fields.Date.context_today)
    expected_delivery_date = fields.Date(string='Expected Delivery Date')
    item_ids = fields.One2many('sf.laundry.item', 'order_id', string='Items')
    total = fields.Monetary(string='Total', compute='_compute_total', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    pickup_date = fields.Datetime(string='Pickup Date')
    delivery_date = fields.Datetime(string='Delivery Date')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('item_ids.subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(order.item_ids.mapped('subtotal'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.laundry.order')
            if not vals.get('expected_delivery_date'):
                delay_days = int(self.env['ir.config_parameter'].sudo().get_param(
                    'sf_laundry.expected_delivery_days', '3'
                ))
                deposit = vals.get('deposit_date') or fields.Date.context_today(self)
                vals['expected_delivery_date'] = deposit + timedelta(days=delay_days)
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_laundry.group_sf_laundry_manager'):
            raise UserError(_('Only a laundry manager can perform this action.'))

    def _check_lost_items(self):
        lost = self.item_ids.filtered(lambda i: i.state == 'lost')
        if lost:
            raise UserError(_('Item %s is lost. The order cannot be delivered until it is regularized.') % lost[0].name)

    def write(self, vals):
        if any(order.state == 'delivered' for order in self) and vals.get('item_ids'):
            raise UserError(_('Items of a delivered order cannot be modified.'))
        return super().write(vals)

    def action_receive(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft orders can be received.'))
        if not self.item_ids:
            raise UserError(_('The order has no items.'))
        self.state = 'received'
        self.pickup_date = fields.Datetime.now()
        self.item_ids.write({'state': 'received'})

    def action_start(self):
        self.ensure_one()
        if self.state != 'received':
            raise UserError(_('Only received orders can be started.'))
        self.state = 'in_progress'
        self.item_ids.write({'state': 'in_progress'})

    def action_ready(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress orders can be marked ready.'))
        self.item_ids.write({'state': 'ready'})
        self.state = 'ready'

    def action_deliver(self):
        self.ensure_one()
        if self.state != 'ready':
            raise UserError(_('Only ready orders can be delivered.'))
        self._check_lost_items()
        self.item_ids.write({'state': 'delivered'})
        self.state = 'delivered'
        self.delivery_date = fields.Datetime.now()
        return self.env.ref('sf_laundry.report_delivery_ticket').report_action(self)

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('in_progress', 'ready', 'delivered'):
            raise UserError(_('A %s order cannot be cancelled.') % self.state)
        if self.state == 'received':
            self._check_manager()
        self.state = 'cancelled'

    def _cron_daily_alerts(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            overdue = scoped.env['sf.laundry.order'].search([
                ('state', 'in', ('draft', 'received', 'in_progress', 'ready')),
            ]).filtered(lambda o: o.expected_delivery_date and o.expected_delivery_date < today)
            for order in overdue:
                order._sf_check_todo(
                    todo_type,
                    'Order %s is overdue for delivery' % order.name,
                    'Reminder: the expected delivery date (%s) has passed.' % order.expected_delivery_date,
                )
            slow_hours = int(scoped.env['ir.config_parameter'].sudo().get_param(
                'sf_laundry.slow_threshold_hours', '72'
            ))
            slow = scoped.env['sf.laundry.item'].search([
                ('state', '=', 'in_progress'),
            ]).filtered(
                lambda i: i.write_date and i.write_date < (fields.Datetime.now() - timedelta(hours=slow_hours))
            )
            for item in slow:
                item._sf_check_todo(
                    todo_type,
                    'Item %s in progress for more than %s hours' % (item.name, slow_hours),
                    'Reminder: the item has been in progress for more than %s hours.' % slow_hours,
                )

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.laundry.activity.mixin'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.laundry.activity.mixin'

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
