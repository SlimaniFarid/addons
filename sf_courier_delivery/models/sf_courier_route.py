# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfCourierRoute(models.Model):
    _name = 'sf.courier.route'
    _description = 'Courier Route'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.courier.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    courier_id = fields.Many2one('res.partner', string='Courier', required=True, ondelete='restrict')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    delivery_ids = fields.One2many('sf.courier.delivery', 'route_id', string='Deliveries')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.courier.route')
        return super().create(vals_list)

    def action_plan(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft routes can be planned.'))
        self.state = 'planned'

    def action_start(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned routes can be started.'))
        self.state = 'in_progress'
        self.delivery_ids.filtered(lambda d: d.state == 'assigned').write({'state': 'in_transit'})

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress routes can be closed.'))
        open_deliveries = self.delivery_ids.filtered(
            lambda d: d.state in ('draft', 'assigned', 'in_transit', 'failed')
        )
        if open_deliveries:
            raise UserError(_('The route has open deliveries and cannot be closed.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('A done route cannot be cancelled.'))
        if self.delivery_ids.filtered(lambda d: d.state in ('in_transit', 'delivered')):
            raise UserError(_('The route has active deliveries and cannot be cancelled.'))
        self.delivery_ids.filtered(lambda d: d.state == 'assigned').write({'state': 'draft'})
        self.state = 'cancelled'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.courier.activity.mixin'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

