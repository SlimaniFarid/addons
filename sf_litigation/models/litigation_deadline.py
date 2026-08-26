# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LitigationDeadline(models.Model):
    _name = 'sf.litigation.deadline'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Procedural Deadline'
    _order = 'due_date, id'

    name = fields.Char(string='Reference', required=True, index=True,
                       tracking=True)
    case_id = fields.Many2one('sf.litigation.case', string='Case',
                              required=True, ondelete='cascade', index=True)
    deadline_type = fields.Selection([
        ('hearing', 'Hearing'),
        ('filing', 'Filing'),
        ('appeal', 'Appeal'),
        ('response', 'Response'),
        ('other', 'Other'),
    ], string='Deadline type', required=True, tracking=True)
    due_date = fields.Date(string='Due date', required=True, tracking=True,
                           index=True)
    alert_days = fields.Integer(string='Alert days before due date')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('active', 'Active'),
        ('met', 'Met'),
        ('missed', 'Missed'),
    ], string='Status', default='active', required=True, tracking=True,
       index=True)
    met_date = fields.Date(string='Met date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.litigation.deadline')
            vals['name'] = 'DDL-%s' % seq
        return super().create(vals)

    def action_mark_met(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active deadlines can be marked as met.'))
        self.write({'state': 'met', 'met_date': fields.Date.today()})

    def _check_litigation_deadlines(self):
        today = fields.Date.today()
        companies = self.env['res.company'].search([])
        for company in companies:
            deadlines = self.with_company(company).search([
                ('state', '=', 'active'),
                ('company_id', '=', company.id),
            ])
            for rec in deadlines:
                if rec.due_date and rec.due_date < today and \
                        not rec.met_date:
                    rec.state = 'missed'
                alert_days = rec.alert_days or \
                    rec.company_id.sf_litigation_alert_days
                if rec.state == 'active' and rec.due_date and \
                        rec.due_date - timedelta(days=alert_days) <= today:
                    existing = rec.activity_ids.filtered(
                        lambda a:
                        a.activity_type_id ==
                        self.env.ref('mail.mail_activity_data_todo')
                        and a.state != 'done')
                    if existing:
                        continue
                    rec.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Procedural deadline: %s') % rec.name,
                        date_deadline=rec.due_date)