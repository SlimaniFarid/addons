# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgValue(models.Model):
    _name = 'sf.esg.value'
    _description = 'ESG Value'
    _order = 'period_id desc, indicator_id'

    period_id = fields.Many2one('sf.esg.period', string='Period',
                                required=True, ondelete='cascade',
                                index=True)
    indicator_id = fields.Many2one('sf.esg.indicator',
                                   string='Indicator', required=True,
                                   ondelete='restrict', index=True)
    category = fields.Selection(related='indicator_id.category',
                                string='Category', store=True,
                                readonly=True)
    value = fields.Float(string='Value', required=True)
    target = fields.Float(string='Target')
    variation = fields.Float(string='Variation (%)',
                             compute='_compute_variation', store=True)
    achieved = fields.Float(string='Target achievement',
                            compute='_compute_variation', store=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('period_indicator_company_uniq',
         'UNIQUE(period_id, indicator_id, company_id)',
         _('This indicator already has a value for this period and '
           'company.')),
    ]

    @api.depends('period_id.state', 'value', 'target')
    def _compute_variation(self):
        for value in self:
            achieved = 0.0
            if value.target and value.target > 0:
                achieved = value.value / value.target
            variation = 0.0
            if value.period_id.state == 'approved':
                previous = self._get_previous_value(value)
                if previous and previous.value:
                    variation = (value.value - previous.value) \
                        / previous.value * 100
            value.achieved = achieved
            value.variation = variation

    def _get_previous_value(self, value):
        previous_period = self.env['sf.esg.period'].search([
            ('company_id', '=', value.company_id.id),
            ('state', '=', 'approved'),
            ('date_from', '<', value.period_id.date_from),
        ], order='date_from desc', limit=1)
        if not previous_period:
            return self.browse()
        return self.search([
            ('period_id', '=', previous_period.id),
            ('indicator_id', '=', value.indicator_id.id),
        ], limit=1)