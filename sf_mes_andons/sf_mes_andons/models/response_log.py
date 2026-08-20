# -*- coding: utf-8 -*-
from odoo import fields, models, _


class AndonResponseLog(models.Model):
    _name = 'sf.andon.response.log'
    _description = 'Andon Response Log'
    _order = 'create_date desc'

    call_id = fields.Many2one('sf.andon.call', string='Andon Call', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    action = fields.Selection([
        ('acknowledged', 'Acknowledged'),
        ('started', 'Started Work'),
        ('updated', 'Status Updated'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
        ('commented', 'Comment Added'),
        ('reassigned', 'Reassigned'),
    ], string='Action', required=True)
    comment = fields.Text(string='Comment')
    previous_state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Previous State')
    new_state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='New State')
    create_date = fields.Datetime(string='Timestamp', readonly=True)