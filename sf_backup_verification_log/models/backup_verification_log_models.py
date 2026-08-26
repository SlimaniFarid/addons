# -*- coding: utf-8 -*-
"""Backup Verification Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBackupLog(models.Model):
    _name = 'sf.backup.log'
    _description = 'Backup Log Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    backup_type = fields.Selection([
        ('full', 'Full'),
        ('incremental', 'Incremental'),
        ('differential', 'Differential'),
        ], string='Type', required=True, default=full)
    system = fields.Char(string='System / DB', required=True)
    run_at = fields.Datetime(string='Run At', default=fields.Datetime.now)
    size_gb = fields.Float(string='Size (GB)')
    verified = fields.Boolean(string='Verified')
    restore_tested = fields.Boolean(string='Restore Tested')
    issues = fields.Text(string='Issues')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ], string='Status', default='running', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.backup.log') or 'NEW'
        return super().create(vals_list)

    def action_success(self):
        self.write({'state': 'success'})

    def action_failed(self):
        self.write({'state': 'failed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.backup.log'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
