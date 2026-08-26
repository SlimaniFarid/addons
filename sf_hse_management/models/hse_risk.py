# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HseRisk(models.Model):
    _name = 'sf.hse.risk'
    _description = 'HSE Risk'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'risk_level desc'

    name = fields.Char(string='Name', required=True)
    category = fields.Selection([
        ('operational', 'Operational'),
        ('safety', 'Safety'),
        ('environmental', 'Environmental'),
        ('hygiene', 'Hygiene'),
        ('fire', 'Fire'),
    ], string='Category', default='safety')
    location = fields.Char(string='Location')
    probability = fields.Integer(string='Probability', default=2)
    severity = fields.Integer(string='Severity', default=2)
    risk_level = fields.Integer(string='Risk Level',
                                compute='_compute_risk_level', store=True)
    risk_class = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme'),
    ], string='Risk Class', compute='_compute_risk_level', store=True)
    mitigation = fields.Text(string='Mitigation')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.depends('probability', 'severity')
    def _compute_risk_level(self):
        for risk in self:
            risk.risk_level = risk.probability * risk.severity
            if risk.risk_level <= 4:
                risk.risk_class = 'low'
            elif risk.risk_level <= 8:
                risk.risk_class = 'medium'
            elif risk.risk_level <= 16:
                risk.risk_class = 'high'
            else:
                risk.risk_class = 'extreme'

    @api.constrains('probability', 'severity')
    def _check_matrix(self):
        for risk in self:
            if risk.probability < 1 or risk.probability > 5:
                raise UserError(
                    _('Probability must be between 1 and 5.'))
            if risk.severity < 1 or risk.severity > 5:
                raise UserError(_('Severity must be between 1 and 5.'))

    def unlink(self):
        for risk in self:
            if risk.active:
                raise UserError(
                    _('An active risk cannot be deleted. Archive it '
                      'instead.'))
        return super().unlink()