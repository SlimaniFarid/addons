# -*- coding: utf-8 -*-
from odoo import fields, models, _


class AndonEscalationRule(models.Model):
    _name = 'sf.andon.escalation.rule'
    _description = 'Andon Escalation Rule'
    _order = 'call_type, level'

    name = fields.Char(string='Name', required=True)
    call_type = fields.Selection([
        ('quality', 'Quality Issue'),
        ('maintenance', 'Maintenance'),
        ('material', 'Material Shortage'),
        ('safety', 'Safety'),
        ('process', 'Process Deviation'),
        ('other', 'Other'),
    ], string='Call Type', required=True)
    level = fields.Integer(string='Escalation Level', required=True, default=1)
    trigger_delay = fields.Integer(string='Trigger Delay (minutes)', default=15,
                                   help='Time before escalating to this level')
    user_ids = fields.Many2many('res.users', string='Notify Users')
    group_ids = fields.Many2many('res.groups', string='Notify Groups')
    send_email = fields.Boolean(string='Send Email', default=True)
    send_sms = fields.Boolean(string='Send SMS', default=False)
    require_acknowledgment = fields.Boolean(string='Require Acknowledgment', default=True)
    auto_escalate = fields.Boolean(string='Auto-Escalate to Next Level', default=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('type_level_uniq', 'unique(call_type, level)', 'Only one rule per call type and level.'),
    ]