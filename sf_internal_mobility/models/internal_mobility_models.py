# -*- coding: utf-8 -*-
"""Internal Job Postings & Mobility models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInternalPosting(models.Model):
    _name = 'sf.internal.posting'
    _description = 'Internal Job Posting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Position', required=True)
    department = fields.Char(string='Department')
    description = fields.Html(string='Description')
    open_until = fields.Date(string='Open Until')
    hiring_manager_id = fields.Many2one('res.users', string='Hiring Manager')
    applications = fields.Integer(string='Applications')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('posted', 'Posted'),
        ('screening', 'Screening'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='posted', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.internal.posting') or 'NEW'
        return super().create(vals_list)

    def action_screening(self):
        self.write({'state': 'screening'})

    def action_filled(self):
        self.write({'state': 'filled'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.internal.posting'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
