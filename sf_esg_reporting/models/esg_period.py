# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EsgPeriod(models.Model):
    _name = 'sf.esg.period'
    _description = 'ESG Period'
    _order = 'date_from desc'

    name = fields.Char(string='Number', required=True, index=True)
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    submitted_date = fields.Datetime(string='Submitted on')
    approved_date = fields.Datetime(string='Approved on')
    approved_by = fields.Many2one('res.users', string='Approved by',
                                  readonly=True)
    value_ids = fields.One2many('sf.esg.value', 'period_id',
                                string='Values')
    total_value = fields.Float(string='Total value',
                               compute='_compute_total_value',
                               store=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    def _compute_total_value(self):
        for period in self:
            period.total_value = sum(period.value_ids.mapped('value'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.esg.period')
            year = fields.Date.context_today(self).year
            vals['name'] = 'ESG-%s-P%s' % (year, seq)
        return super().create(vals)

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft periods can be submitted.'))
        self.write({
            'state': 'submitted',
            'submitted_date': fields.Datetime.now(),
        })

    def action_approve(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_esg_reporting.group_esg_manager'):
            raise UserError(_('Only ESG managers can approve periods.'))
        if self.state != 'submitted':
            raise UserError(_('Only submitted periods can be approved.'))
        self.write({
            'state': 'approved',
            'approved_date': fields.Datetime.now(),
            'approved_by': self.env.user.id,
        })

    def action_close(self):
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_('Only approved periods can be closed.'))
        self.state = 'closed'