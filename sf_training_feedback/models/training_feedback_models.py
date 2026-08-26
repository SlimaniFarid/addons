# -*- coding: utf-8 -*-
"""Training Feedback Collection models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTrainingFeedback(models.Model):
    _name = 'sf.training.feedback'
    _description = 'Training Feedback'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    session_label = fields.Char(string='Training Session', required=True)
    employee_id = fields.Many2one('hr.employee', string='Participant', required=True)
    rating = fields.Selection([
        ('1', '1 - Poor'),
        ('2', '2'),
        ('3', '3 - Average'),
        ('4', '4 - Good'),
        ('5', '5 - Excellent'),
        ], string='Rating', required=True)
    trainer_rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ], string='Trainer Rating')
    comments = fields.Text(string='Comments')
    would_recommend = fields.Boolean(string='Would Recommend')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('collected', 'Collected'),
        ('reviewed', 'Reviewed'),
        ], string='Status', default='collected', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.training.feedback') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.training.feedback'

    def action_refresh_business(self):
        """Pull employee tenure and status."""
        for rec in self:
            emp = getattr(rec, 'employee_id', False)
            if not emp:
                continue
            hire = emp.first_contract_date or False
            years = ''
            if hire:
                delta = (fields.Date.context_today(rec) - hire).days
                years = ', tenure {:.1f}y'.format(delta / 365.25)
            rec.message_post(body=_('{name} ({dept}){tenure}, '
                                    'active={act}.').format(
                name=emp.name,
                dept=emp.department_id.name or '-',
                tenure=years,
                act=emp.active))
        return True
