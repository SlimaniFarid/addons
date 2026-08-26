# -*- coding: utf-8 -*-
"""PO Approval Matrix models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPoApprovalLevel(models.Model):
    _name = 'sf.po.approval.level'
    _description = 'Approval Level'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    level_name = fields.Char(string='Level', required=True)
    min_amount = fields.Monetary(string='From Amount')
    max_amount = fields.Monetary(string='To Amount (0=unlimited)')
    approver_id = fields.Many2one('res.users', string='Approver', required=True)
    delegate_id = fields.Many2one('res.users', string='Delegate')
    active = fields.Boolean(string='Active', default=True)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('archived', 'Archived'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.po.approval.level') or 'NEW'
        return super().create(vals_list)

    def action_archived(self):
        self.write({'state': 'archived'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.po.approval.level'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
