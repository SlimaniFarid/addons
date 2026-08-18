# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AndonCall(models.Model):
    _name = 'sf.andon.call'
    _description = 'Andon Call'
    _rec_name = 'display_name'
    _order = 'priority desc, create_date desc'

    display_name = fields.Char(string='Reference', compute='_compute_display_name', store=True)
    station_id = fields.Many2one('sf.andon.station', string='Station', required=True, ondelete='cascade')
    work_order_id = fields.Many2one('sf.mes.work.order', string='Work Order', ondelete='set null')
    call_type = fields.Selection([
        ('quality', 'Quality Issue'),
        ('maintenance', 'Maintenance'),
        ('material', 'Material Shortage'),
        ('safety', 'Safety'),
        ('process', 'Process Deviation'),
        ('other', 'Other'),
    ], string='Type', required=True, default='quality')
    severity = fields.Selection([
        ('low', 'Low - Informational'),
        ('medium', 'Medium - Attention Needed'),
        ('high', 'High - Urgent'),
        ('critical', 'Critical - Line Stop'),
    ], string='Severity', required=True, default='medium')
    priority = fields.Integer(string='Priority', compute='_compute_priority', store=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='new', tracking=True)
    assigned_user_id = fields.Many2one('res.users', string='Assigned To')
    responder_ids = fields.Many2many('res.users', string='Notified Responders')
    escalation_level = fields.Integer(string='Escalation Level', default=0)
    created_by_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    create_date = fields.Datetime(string='Created', readonly=True)
    acknowledged_date = fields.Datetime(string='Acknowledged')
    resolved_date = fields.Datetime(string='Resolved')
    closed_date = fields.Datetime(string='Closed')
    response_time = fields.Float(string='Response Time (min)', compute='_compute_times', store=True)
    resolution_time = fields.Float(string='Resolution Time (min)', compute='_compute_times', store=True)
    root_cause = fields.Text(string='Root Cause')
    corrective_action = fields.Text(string='Corrective Action')
    preventive_action = fields.Text(string='Preventive Action')

    @api.depends('station_id', 'create_date', 'id')
    def _compute_display_name(self):
        for call in self:
            call.display_name = f"ANDON-{call.id:06d}"

    @api.depends('severity', 'call_type')
    def _compute_priority(self):
        severity_map = {'low': 10, 'medium': 50, 'high': 80, 'critical': 100}
        type_bonus = {'safety': 20, 'quality': 10, 'maintenance': 5, 'material': 5}
        for call in self:
            call.priority = severity_map.get(call.severity, 10) + type_bonus.get(call.call_type, 0)

    @api.depends('acknowledged_date', 'resolved_date', 'create_date')
    def _compute_times(self):
        for call in self:
            if call.acknowledged_date and call.create_date:
                delta = call.acknowledged_date - call.create_date
                call.response_time = delta.total_seconds() / 60.0
            else:
                call.response_time = 0.0
            if call.resolved_date and call.create_date:
                delta = call.resolved_date - call.create_date
                call.resolution_time = delta.total_seconds() / 60.0
            else:
                call.resolution_time = 0.0

    def action_acknowledge(self):
        for call in self:
            if call.state == 'new':
                call.state = 'acknowledged'
                call.acknowledged_date = fields.Datetime.now()
                call.assigned_user_id = self.env.user

    def action_start_work(self):
        for call in self:
            if call.state in ('new', 'acknowledged'):
                call.state = 'in_progress'
                if not call.assigned_user_id:
                    call.assigned_user_id = self.env.user

    def action_resolve(self):
        for call in self:
            if call.state in ('acknowledged', 'in_progress'):
                call.state = 'resolved'
                call.resolved_date = fields.Datetime.now()

    def action_close(self):
        for call in self:
            if call.state == 'resolved':
                call.state = 'closed'
                call.closed_date = fields.Datetime.now()

    def action_cancel(self):
        for call in self:
            if call.state not in ('closed', 'cancelled'):
                call.state = 'cancelled'

    def action_escalate(self):
        for call in self:
            call.escalation_level += 1
            # Notify next level responders based on escalation rules
            rules = self.env['sf.andon.escalation.rule'].search([
                ('call_type', '=', call.call_type),
                ('level', '=', call.escalation_level),
            ])
            for rule in rules:
                call.responder_ids = [(4, u.id) for u in rule.user_ids]