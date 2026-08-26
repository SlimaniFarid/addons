# -*- coding: utf-8 -*-
from odoo import fields, models, _, api
from odoo.exceptions import UserError


class EnergyObjective(models.Model):
    _name = 'sf.energy.objective'
    _inherit = ['mail.thread']
    _description = 'Energy Reduction Objective'
    _order = 'year desc, site_id'

    site_id = fields.Many2one('sf.energy.site', string='Site',
                              required=True)
    utility_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('water', 'Water'),
    ], string='Utility', required=True)
    year = fields.Integer(string='Year', required=True,
                          default=lambda self: fields.Date.today().year)
    target_amount = fields.Float(string='Target Consumption',
                                 required=True)
    period = fields.Selection([
        ('month', 'Monthly'),
        ('year', 'Yearly'),
    ], string='Period', default='month', required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('achieved', 'Achieved'),
        ('expired', 'Expired'),
    ], string='Status', default='active')
    achieved_date = fields.Date(string='Achieved Date')
    notes = fields.Text(string='Notes')

    @api.constrains('target_amount')
    def _check_target(self):
        for obj in self:
            if obj.target_amount <= 0:
                raise UserError(
                    _('The target consumption must be positive.'))

    def action_close(self):
        for obj in self:
            obj.state = 'expired'

    def _get_period_consumption(self, date_from, date_to):
        self.ensure_one()
        meters = self.env['sf.energy.meter'].search([
            ('site_id', '=', self.site_id.id),
            ('utility_type', '=', self.utility_type),
        ])
        return sum(
            r.consumption
            for m in meters
            for r in m.reading_ids
            if r.state == 'confirmed'
            and r.date >= date_from and r.date <= date_to
        )

    def _check_objective_breach(self):
        today = fields.Date.today()
        for obj in self.search([('state', '=', 'active')]):
            if obj.period == 'month':
                from odoo.tools.date_utils import start_of, end_of
                date_from = start_of(today, 'month').date()
                date_to = end_of(today, 'month').date()
            else:
                date_from = today.replace(month=1, day=1)
                date_to = today.replace(month=12, day=31)
            consumption = obj._get_period_consumption(date_from, date_to)
            if consumption > obj.target_amount:
                obj.activity_schedule(
                    'mail.mail_activity_data_todo',
                    _('Consumption (%s) exceeded the target (%s) for '
                      '%s.') % (consumption, obj.target_amount, obj.site_id.name),
                    user_id=obj.env.user.id)
            if obj.period == 'month' and consumption > 0 \
                    and consumption <= obj.target_amount:
                obj.write({'state': 'achieved',
                           'achieved_date': today})