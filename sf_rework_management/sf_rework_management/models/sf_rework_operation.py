# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfReworkOperation(models.Model):
    _name = 'sf.rework.operation'
    _description = 'Rework Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rework.management.activity.mixin']
    _order = 'id asc'

    name = fields.Char(string='Name', required=True)
    order_id = fields.Many2one('sf.rework.order', string='Rework Order',
                               required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Operator')
    operator_name = fields.Char(string='Operator Name')
    hours = fields.Float(string='Hours', required=True)
    hourly_rate = fields.Monetary(string='Hourly Rate', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', store=True, readonly=True)
    done = fields.Boolean(string='Done', default=False)
    description = fields.Text(string='Description')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_hours_positive', 'CHECK (hours >= 0)',
         'The operation hours cannot be negative.'),
    ]

    @api.constrains('hours')
    def _check_hours(self):
        for operation in self:
            if operation.hours < 0:
                raise ValidationError(_('The operation hours cannot be negative.'))