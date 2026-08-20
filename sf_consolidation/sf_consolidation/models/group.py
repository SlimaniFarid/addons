# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ConsolidationGroup(models.Model):
    _name = 'sf.consolidation.group'
    _description = 'Consolidation Group'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    company_ids = fields.Many2many('res.company', string='Companies',
                                   required=True)
    period_ids = fields.One2many('sf.consolidation.period', 'group_id',
                                 string='Periods')
    currency_id = fields.Many2one('res.currency', string='Group Currency',
                                  default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Group code must be unique.'),
    ]

    def action_create_period(self, date_from, date_to):
        self.ensure_one()
        return self.env['sf.consolidation.period'].create({
            'group_id': self.id,
            'date_from': date_from,
            'date_to': date_to,
            'name': '%s %s-%s' % (self.name, date_from, date_to),
        })