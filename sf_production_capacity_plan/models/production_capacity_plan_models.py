# -*- coding: utf-8 -*-
"""Production Capacity Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_capacity_plan(models.Model):
    _name = 'sf.production_capacity_plan'
    _description = 'Production Capacity Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center', required=True)
    period = fields.Char(string='Period', required=True)
    available_hours = fields.Float(string='Available Hours')
    planned_hours = fields.Float(string='Planned Load')
    utilization_percent = fields.Float(string='Utilization %')
    overtime_needed = fields.Float(string='Overtime Needed (h)')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.production_capacity_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.production_capacity_plan'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.production_capacity_plan'

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
