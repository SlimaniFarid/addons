# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ProjectBudgetItem(models.Model):
    _name = 'sf.project.budget.item'
    _description = 'Project Budget Item'
    _rec_name = 'category'
    _order = 'project_id, type'

    project_id = fields.Many2one('project.project', string='Project',
                                 required=True, ondelete='cascade')
    type = fields.Selection([
        ('revenue', 'Revenue'),
        ('cost', 'Cost'),
    ], string='Type', default='revenue', required=True)
    category = fields.Char(string='Category', required=True)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    note = fields.Text(string='Notes')