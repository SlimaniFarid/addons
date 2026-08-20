# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfCourierDeliveryAttempt(models.Model):
    _name = 'sf.courier.delivery.attempt'
    _description = 'Courier Delivery Attempt'
    _order = 'attempt_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    delivery_id = fields.Many2one('sf.courier.delivery', string='Delivery', required=True, ondelete='cascade')
    attempt_date = fields.Datetime(string='Attempt Date', default=fields.Datetime.now)
    result = fields.Selection([
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ], string='Result', required=True)
    failure_reason = fields.Selection([
        ('absent', 'Recipient Absent'),
        ('wrong_address', 'Wrong Address'),
        ('refused', 'Recipient Refused'),
        ('damaged', 'Parcel Damaged'),
        ('other', 'Other'),
    ], string='Failure Reason')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.courier.delivery.attempt')
            if not vals.get('company_id') and vals.get('delivery_id'):
                delivery = self.env['sf.courier.delivery'].browse(vals['delivery_id'])
                vals['company_id'] = delivery.company_id.id
        return super().create(vals_list)