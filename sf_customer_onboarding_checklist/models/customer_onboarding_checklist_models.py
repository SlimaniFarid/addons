# -*- coding: utf-8 -*-
"""Customer Onboarding Checklist Runner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_onboarding_checklist(models.Model):
    _name = 'sf.customer_onboarding_checklist'
    _description = 'Customer Onboarding Checklist Runner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    checklist_item = fields.Char(string='Checklist Item', required=True)
    step_type = fields.Selection([
        ('document', 'Document'),
        ('setup', 'Account Setup'),
        ('training', 'Training'),
        ('go_live', 'Go-Live'),
        ], string='Type', required=True)
    completed = fields.Boolean(string='Completed')
    owner_id = fields.Many2one('res.users', string='Owner')
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
                    'sf.customer_onboarding_checklist') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer_onboarding_checklist'

    active = fields.Boolean(string='Active', default=True)
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.customer_onboarding_checklist'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
