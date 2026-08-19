# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class RouteTerritory(models.Model):
    _name = 'sf.route.territory'
    _description = 'Sales Territory'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    region = fields.Char(string='Region')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('name_company_uniq', 'UNIQUE (name, company_id)',
         'A territory name must be unique per company.'),
    ]

    def unlink(self):
        tours = self.env['sf.route.tour'].search([
            ('territory_id', 'in', self.ids),
        ])
        if tours:
            raise UserError(
                _('A territory with planned routes cannot be deleted.'))
        return super().unlink()


class RouteObjective(models.Model):
    _name = 'sf.route.objective'
    _description = 'Sales Territory Objective'
    _order = 'period_start'

    territory_id = fields.Many2one('sf.route.territory',
                                   string='Territory', required=True)
    period_start = fields.Date(string='Start Date', required=True)
    period_end = fields.Date(string='End Date', required=True)
    target_visits = fields.Integer(string='Target Visits', default=0)
    target_orders = fields.Integer(string='Target Orders', default=0)
    target_revenue = fields.Monetary(string='Target Revenue', default=0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True,
                                  default=lambda self:
                                  self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.constrains('period_start', 'period_end')
    def _check_period(self):
        for obj in self:
            if obj.period_end < obj.period_start:
                raise UserError(
                    _('The end date must be after the start date.'))