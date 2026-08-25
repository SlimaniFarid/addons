# -*- coding: utf-8 -*-
"""Remote Work Request Workflow models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRemoteWork(models.Model):
    _name = 'sf.remote.work'
    _description = 'Remote Work Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    days_count = fields.Integer(string='Days')
    equipment_ready = fields.Boolean(string='Equipment Ready')
    manager_id = fields.Many2one('res.users', string='Manager')
    reason = fields.Text(string='Reason')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.remote.work') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.remote.work'

    active = fields.Boolean(string='Active', default=True)
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

