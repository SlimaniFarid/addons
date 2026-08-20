# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfCourierOrder(models.Model):
    _name = 'sf.courier.order'
    _description = 'Courier Request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.courier.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    pickup_address = fields.Text(string='Pickup Address')
    delivery_address = fields.Text(string='Delivery Address')
    scheduled_from = fields.Datetime(string='Scheduled From')
    scheduled_to = fields.Datetime(string='Scheduled To')
    type = fields.Selection([
        ('pickup_delivery', 'Pickup & Delivery'),
        ('delivery_only', 'Delivery Only'),
        ('pickup_only', 'Pickup Only'),
    ], string='Request Type', required=True, default='pickup_delivery')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    delivery_ids = fields.One2many('sf.courier.delivery', 'order_id', string='Deliveries')
    delivery_count = fields.Integer(string='Deliveries', compute='_compute_delivery_count', store=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='set null')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('delivery_ids')
    def _compute_delivery_count(self):
        for order in self:
            order.delivery_count = len(order.delivery_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.courier.order')
        return super().create(vals_list)

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft requests can be confirmed.'))
        self.state = 'confirmed'

    def action_done(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed requests can be marked done.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('A done request cannot be cancelled.'))
        if self.delivery_ids.filtered(lambda d: d.state in ('in_transit', 'delivered')):
            raise UserError(_('The request has active deliveries and cannot be cancelled.'))
        self.state = 'cancelled'

    def action_view_deliveries(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Deliveries',
            'res_model': 'sf.courier.delivery',
            'view_mode': 'list,form',
            'domain': [('order_id', '=', self.id)],
        }

    def action_invoice(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'done'):
            raise UserError(_('Only confirmed or done requests can be invoiced.'))
        if self.invoice_id:
            raise UserError(_('The request has already been invoiced.'))
        delivered = self.delivery_ids.filtered(lambda d: d.state == 'delivered')
        if not delivered:
            raise UserError(_('There are no delivered deliveries to invoice.'))
        account_id = self.env['ir.config_parameter'].sudo().get_param(
            'sf_courier_delivery.revenue_account_id')
        if not account_id:
            account = self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', self.company_id.id),
            ], limit=1)
            account_id = account.id if account else False
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.company_id.id),
            ('type', '=', 'sale'),
        ], limit=1)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'journal_id': journal.id if journal else False,
            'invoice_line_ids': [(0, 0, {
                'name': 'Delivery services: %s' % self.name,
                'quantity': 1,
                'price_unit': sum(delivered.mapped('price')),
                'account_id': int(account_id) if account_id else False,
            })],
        })
        self.invoice_id = invoice.id
        return True

    def _cron_daily_alerts(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            now = fields.Datetime.now()
            overdue = scoped.env['sf.courier.delivery'].search([
                ('state', 'in', ('assigned', 'in_transit')),
                ('company_id', '=', company.id),
            ]).filtered(
                lambda d: d.order_id.scheduled_to and d.order_id.scheduled_to < now
            )
            for delivery in overdue:
                delivery._sf_check_todo(
                    todo_type,
                    'Delivery %s is overdue' % delivery.name,
                    'Reminder: the scheduled time window has passed.',
                )
            unresolved = scoped.env['sf.courier.delivery'].search([
                ('state', '=', 'failed'),
                ('company_id', '=', company.id),
            ])
            for delivery in unresolved:
                delivery._sf_check_todo(
                    todo_type,
                    'Delivery %s is unresolved' % delivery.name,
                    'Reminder: the failed delivery still awaits a decision.',
                )