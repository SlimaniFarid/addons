# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfAqlPlan(models.Model):
    _name = 'sf.aql.plan'
    _description = 'AQL Sampling Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_level asc, lot_size_min asc'

    name = fields.Char(string='Name', required=True, copy=False)
    inspection_level = fields.Selection([
        ('I', 'Level I'),
        ('II', 'Level II'),
        ('III', 'Level III'),
    ], string='Inspection Level', required=True, default='II')
    lot_size_min = fields.Integer(string='Lot Size Min', required=True, default=0)
    lot_size_max = fields.Integer(string='Lot Size Max', required=True, default=1)
    sample_size = fields.Integer(string='Sample Size', required=True, default=1)
    accept_number = fields.Integer(string='Accept Number', required=True, default=0)
    reject_number = fields.Integer(string='Reject Number', required=True, default=1)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_lot_size_range',
         'CHECK (lot_size_max >= lot_size_min)',
         'The maximum lot size cannot be lower than the minimum lot size.'),
        ('check_sample_positive',
         'CHECK (sample_size > 0)',
         'The sample size must be greater than zero.'),
        ('check_accept_not_negative',
         'CHECK (accept_number >= 0)',
         'The accept number cannot be negative.'),
        ('check_reject_greater_accept',
         'CHECK (reject_number > accept_number)',
         'The reject number must be greater than the accept number.'),
    ]

    @api.constrains('lot_size_min', 'lot_size_max', 'sample_size', 'reject_number',
                    'accept_number')
    def _check_plan(self):
        for plan in self:
            if plan.lot_size_max < plan.lot_size_min:
                raise ValidationError(_('The maximum lot size cannot be lower than the minimum lot size.'))
            if plan.sample_size <= 0:
                raise ValidationError(_('The sample size must be greater than zero.'))
            if plan.accept_number < 0:
                raise ValidationError(_('The accept number cannot be negative.'))
            if plan.reject_number <= plan.accept_number:
                raise ValidationError(_('The reject number must be greater than the accept number.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.aql.plan')
        return super().create(vals_list)