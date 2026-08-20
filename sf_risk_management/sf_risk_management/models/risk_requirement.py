# -*- coding: utf-8 -*-
from odoo import fields, models


class RiskRequirement(models.Model):
    _name = 'sf.risk.requirement'
    _description = 'Regulatory Requirement'
    _order = 'code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    regulation = fields.Selection([
        ('nis2', 'NIS2'),
        ('dora', 'DORA'),
        ('iso27001', 'ISO 27001'),
        ('gdpr', 'GDPR'),
        ('iso9001', 'ISO 9001'),
        ('other', 'Other'),
    ], string='Regulation', default='nis2', required=True)
    description = fields.Text(string='Description')
    risk_ids = fields.Many2many(
        'sf.risk',
        'sf_risk_requirement_m2m', 'requirement_id', 'risk_id',
        string='Risks')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)


class RiskRequirementLink(models.Model):
    _name = 'sf.risk.requirement.link'
    _description = 'Risk Requirement Link'

    requirement_id = fields.Many2one('sf.risk.requirement',
                                     string='Requirement',
                                     ondelete='cascade', required=True)
    risk_id = fields.Many2one('sf.risk', string='Risk',
                              ondelete='cascade', required=True)
    coverage = fields.Selection([
        ('full', 'Full'),
        ('partial', 'Partial'),
        ('none', 'None'),
    ], string='Coverage', default='partial')

    _sql_constraints = [
        ('req_risk_uniq', 'UNIQUE (requirement_id, risk_id)',
         'A requirement can only be linked to a risk once.'),
    ]