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

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.project.budget.item'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.project.budget.item'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
