# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SupplierIssue(models.Model):
    _name = 'sf.supplier.issue'
    _description = 'Supplier Issue'
    _rec_name = 'partner_id'
    _order = 'date desc'

    partner_id = fields.Many2one('res.partner', string='Supplier',
                                 required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    issue_type = fields.Selection([
        ('quality', 'Quality'),
        ('delivery', 'Delivery'),
        ('compliance', 'Compliance'),
        ('other', 'Other'),
    ], string='Type', default='quality', required=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', default='medium')
    description = fields.Text(string='Description')
    resolution = fields.Text(string='Resolution')
    resolved = fields.Boolean(string='Resolved', default=False)
    scorecard_id = fields.Many2one('sf.supplier.scorecard',
                                   string='Linked Scorecard')

    def action_resolve(self):
        for issue in self:
            issue.resolved = True