# -*- coding: utf-8 -*-
"""Line Balancing Review models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLineBalance(models.Model):
    _name = 'sf.line.balance'
    _description = 'Line Balancing Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production / Line', required=True)
    takt_time_seconds = fields.Float(string='Takt Time (s)')
    bottleneck_station = fields.Char(string='Bottleneck Station')
    findings = fields.Html(string='Findings')
    rebalancing_plan = fields.Html(string='Rebalancing Plan')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('actions', 'Actions Defined'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.line.balance') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

    def action_actions(self):
        self.write({'state': 'actions'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.line.balance'

    active = fields.Boolean(string='Active', default=True)
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

