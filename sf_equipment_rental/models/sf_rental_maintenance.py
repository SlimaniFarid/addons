# -*- coding: utf-8 -*-
from odoo import api, _, fields, models
from odoo.exceptions import UserError


class SfRentalMaintenance(models.Model):
    _name = 'sf.rental.maintenance'
    _description = 'Rental Maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rental.activity.mixin']
    _order = 'scheduled_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    equipment_id = fields.Many2one('sf.rental.equipment', string='Equipment', required=True, ondelete='restrict')
    scheduled_date = fields.Date(string='Scheduled Date', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.maintenance')
        return super().create(vals_list)

    def action_schedule(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft maintenance can be scheduled.'))
        if self.equipment_id.state in ('out',):
            raise UserError(_('The equipment is currently rented out.'))
        active = self.search([
            ('equipment_id', '=', self.equipment_id.id),
            ('state', 'in', ('scheduled', 'in_progress')),
            ('id', '!=', self.id),
        ])
        if active:
            raise UserError(_('The equipment already has planned maintenance.'))
        self.state = 'scheduled'
        self.equipment_id.state = 'maintenance'

    def action_start(self):
        self.ensure_one()
        if self.state != 'scheduled':
            raise UserError(_('Only scheduled maintenance can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress maintenance can be completed.'))
        self.state = 'done'
        if self.equipment_id.state == 'maintenance':
            others = self.search([
                ('equipment_id', '=', self.equipment_id.id),
                ('state', 'in', ('scheduled', 'in_progress')),
                ('id', '!=', self.id),
            ])
            if not others:
                self.equipment_id.state = 'available'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('Done maintenance cannot be cancelled.'))
        if self.state == 'scheduled' and self.equipment_id.state == 'maintenance':
            others = self.search([
                ('equipment_id', '=', self.equipment_id.id),
                ('state', 'in', ('scheduled', 'in_progress')),
                ('id', '!=', self.id),
            ])
            if not others:
                self.equipment_id.state = 'available'
        self.state = 'cancelled'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.rental.activity.mixin'

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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.rental.activity.mixin'

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
