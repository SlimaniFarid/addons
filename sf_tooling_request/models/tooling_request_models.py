# -*- coding: utf-8 -*-
"""Tooling Request & Preparation models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfToolingRequest(models.Model):
    _name = 'sf.tooling.request'
    _description = 'Tooling Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    tools_needed = fields.Text(string='Tools / Fixtures Needed', required=True)
    needed_for_date = fields.Date(string='Needed For')
    readiness = fields.Selection([
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('missing', 'Missing Items'),
        ], string='Readiness', default=pending)
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delayed', 'Delayed'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.tooling.request') or 'NEW'
        return super().create(vals_list)

    def action_preparing(self):
        self.write({'state': 'preparing'})

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_delayed(self):
        self.write({'state': 'delayed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.tooling.request'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.tooling.request'

    def action_refresh_business(self):
        """Pull active MO count and average yield."""
        Mos = self.env['mrp.production']
        active = Mos.search([('state', 'in', ('confirmed', 'progress'))])
        done = Mos.search([('state', '=', 'done')], limit=50)
        yields = [(mo.qty_produced / mo.product_qty * 100)
                  for mo in done if mo.product_qty]
        avg_yield = sum(yields) / len(yields) if yields else 0.0
        for rec in self:
            rec.message_post(body=_(
                '{a} active MO(s), avg yield {y:.1f}% on last {d} done.')
                .format(a=len(active), y=avg_yield, d=len(done)))
        return True
