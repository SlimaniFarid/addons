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
    hours = fields.Float(string='Hours', required=True)
    done = fields.Boolean(string='Done', default=False)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_hours_positive', 'CHECK (hours > 0)',
         'The operation hours must be greater than zero.'),
    ]

    @api.constrains('hours')
    def _check_hours(self):
        for operation in self:
            if operation.hours <= 0:
                raise ValidationError(_('The operation hours must be greater than zero.'))