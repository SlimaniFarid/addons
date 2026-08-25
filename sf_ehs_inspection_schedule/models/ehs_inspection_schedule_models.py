# -*- coding: utf-8 -*-
"""EHS Inspection Scheduler models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEhsInspection(models.Model):
    _name = 'sf.ehs.inspection'
    _description = 'EHS Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    site_area = fields.Char(string='Site / Area', required=True)
    inspection_type = fields.Selection([
        ('fire', 'Fire Safety'),
        ('ergonomics', 'Ergonomics'),
        ('chemical', 'Chemical'),
        ('general', 'General Walkthrough'),
        ], string='Type', required=True)
    scheduled_date = fields.Date(string='Scheduled', required=True)
    inspector_id = fields.Many2one('res.users', string='Inspector')
    findings_count = fields.Integer(string='Findings')
    checklist = fields.Html(string='Checklist Results')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('findings_tracked', 'Findings Tracked'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ehs.inspection') or 'NEW'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_findings_tracked(self):
        self.write({'state': 'findings_tracked'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.ehs.inspection'

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

