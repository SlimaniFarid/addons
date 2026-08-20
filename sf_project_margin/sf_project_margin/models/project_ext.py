# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProjectMargin(models.Model):
    _inherit = 'project.project'

    sf_budget_item_ids = fields.One2many('sf.project.budget.item',
                                         'project_id',
                                         string='Budget Items')
    sf_budget_revenue = fields.Float(string='Budget Revenue',
                                     compute='_compute_margin', store=True)
    sf_budget_cost = fields.Float(string='Budget Cost',
                                  compute='_compute_margin', store=True)
    sf_margin = fields.Float(string='Margin', compute='_compute_margin',
                             store=True)
    sf_margin_pct = fields.Float(string='Margin %', compute='_compute_margin',
                                 store=True)
    sf_warning_threshold = fields.Float(string='Warning Threshold %',
                                        default=20.0)
    sf_margin_status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ], string='Margin Status', compute='_compute_margin', store=True)

    @api.depends('sf_budget_item_ids.type', 'sf_budget_item_ids.amount',
                 'sf_warning_threshold')
    def _compute_margin(self):
        for project in self:
            revenue = sum(item.amount for item in project.sf_budget_item_ids
                          if item.type == 'revenue')
            cost = sum(item.amount for item in project.sf_budget_item_ids
                       if item.type == 'cost')
            project.sf_budget_revenue = revenue
            project.sf_budget_cost = cost
            project.sf_margin = revenue - cost
            project.sf_margin_pct = revenue and round(
                (revenue - cost) / revenue * 100, 1) or 0.0
            if project.sf_margin_pct >= project.sf_warning_threshold:
                project.sf_margin_status = 'ok'
            elif project.sf_margin_pct >= project.sf_warning_threshold / 2:
                project.sf_margin_status = 'warning'
            else:
                project.sf_margin_status = 'critical'