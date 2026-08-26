# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SchoolTuition(models.Model):
    _name = 'sf.school.tuition'
    _description = 'Tuition Fee'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tuition', required=True, index=True)
    student_id = fields.Many2one('sf.school.student', string='Student',
                                 required=True, ondelete='restrict',
                                 index=True)
    year_id = fields.Many2one('sf.school.year', string='School year',
                              ondelete='restrict')
    amount = fields.Float(string='Amount', required=True)
    paid_amount = fields.Float(string='Paid amount', default=0.0)
    amount_due = fields.Float(string='Amount due', compute='_compute_due',
                              store=True)
    due_date = fields.Date(string='Due date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ], string='Status', compute='_compute_state', store=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('amount', 'paid_amount')
    def _compute_due(self):
        for rec in self:
            rec.amount_due = rec.amount - rec.paid_amount

    @api.depends('amount', 'paid_amount', 'due_date')
    def _compute_state(self):
        today = fields.Date.today()
        for rec in self:
            if rec.amount > 0 and rec.paid_amount >= rec.amount:
                rec.state = 'paid'
            elif rec.due_date and rec.due_date < today:
                rec.state = 'overdue'
            elif rec.paid_amount > 0:
                rec.state = 'partial'
            else:
                rec.state = 'draft'

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.tuition')
        return super().create(vals)

    def action_receive_payment(self):
        self.ensure_one()
        if self.state == 'paid':
            raise UserError(_('This tuition is already fully paid.'))
        return {
            'name': _('Record Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.school.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_tuition_id': self.id},
        }

    def action_mark_paid(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_school_management.group_school_manager'):
            raise UserError(
                _('Only a School Manager can confirm tuition payments.'))
        self.write({'paid_amount': self.amount})

    def _check_school_alerts(self):
        today = fields.Date.today()
        companies = self.env['res.company'].search([])
        for company in companies:
            alert_days = company.sf_school_alert_days
            cutoff = today - timedelta(days=alert_days)
            tuitions = self.with_company(company).search([
                ('state', '=', 'overdue'),
                ('due_date', '<', cutoff),
            ])
            for rec in tuitions:
                existing = rec.activity_ids.filtered(
                    lambda activity:
                    activity.activity_type_id ==
                    self.env.ref('mail.mail_activity_data_todo') and
                    activity.state != 'done')
                if existing:
                    continue
                manager = self.env['res.users'].search([
                    ('groups_id', 'in', self.env.ref(
                        'sf_school_management.group_school_manager').id),
                ], limit=1)
                user = manager or self.env.user
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Overdue tuition: %s') % rec.name,
                    user_id=user.id)