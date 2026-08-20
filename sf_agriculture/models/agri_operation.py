# -*- coding: utf-8 -*-
from odoo import fields, models


class AgriOperation(models.Model):
    _name = 'sf.agri.operation'
    _description = 'Agricultural Operation'
    _order = 'culture_id, sequence'

    culture_id = fields.Many2one('sf.agri.culture', string='Culture',
                                 required=True, ondelete='cascade',
                                 index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name', required=True)
    operation_type = fields.Selection([
        ('tillage', 'Tillage'),
        ('sowing', 'Sowing'),
        ('irrigation', 'Irrigation'),
        ('fertilization', 'Fertilization'),
        ('protection', 'Protection'),
        ('harvest', 'Harvest'),
        ('other', 'Other'),
    ], string='Type', default='other', required=True)
    planned_date = fields.Date(string='Planned date')
    done_date = fields.Date(string='Done date')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='culture_id.company_id', store=True,
                                 readonly=True)