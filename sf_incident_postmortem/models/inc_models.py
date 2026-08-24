# -*- coding: utf-8 -*-
"""Incident post-mortem models."""
from odoo import api, fields, models, _


class SfIncident(models.Model):
    _name = 'sf.incident'
    _description = 'Operational Incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'detected_at desc'

    name = fields.Char(string='Incident Reference', required=True,
                       copy=False, readonly=True, default='New')
    title = fields.Char(string='Title', required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    severity = fields.Selection([
        ('s1', 'S1 - Critical'), ('s2', 'S2 - Major'),
        ('s3', 'S3 - Minor'), ('s4', 'S4 - Low')],
        required=True, default='s3', tracking=True)
    category = fields.Selection([
        ('it', 'IT / System'), ('production', 'Production'),
        ('logistics', 'Logistics'), ('quality', 'Quality'),
        ('safety', 'Safety'), ('supplier', 'Supplier'),
        ('other', 'Other')], required=True, default='it')
    detected_at = fields.Datetime(string='Detected At', required=True,
                                  default=fields.Datetime.now)
    resolved_at = fields.Datetime(string='Resolved At')
    duration_hours = fields.Float(string='Duration (h)',
                                  compute='_compute_duration', store=True)
    impact = fields.Html(string='Business Impact')
    root_cause = fields.Html(string='Root Cause Analysis')
    lessons_learned = fields.Html(string='Lessons Learned')
    action_ids = fields.One2many('sf.incident.action', 'incident_id',
                                 string='Corrective / Preventive Actions')
    action_count = fields.Integer(compute='_compute_action_count')
    open_actions = fields.Integer(compute='_compute_action_count')
    commander_id = fields.Many2one('res.users', string='Incident Commander')
    state = fields.Selection([
        ('open', 'Open'), ('identified', 'Root Cause Identified'),
        ('actions', 'Actions In Progress'), ('closed', 'Closed')],
        default='open', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.incident') or 'INC-NEW'
        return super().create(vals_list)

    def _compute_duration(self):
        for rec in self:
            if rec.resolved_at and rec.detected_at:
                delta = rec.resolved_at - rec.detected_at
                rec.duration_hours = delta.total_seconds() / 3600.0
            else:
                rec.duration_hours = 0.0

    def _compute_action_count(self):
        for rec in self:
            rec.action_count = len(rec.action_ids)
            rec.open_actions = len(rec.action_ids.filtered(
                lambda a: a.state != 'done'))

    def action_identify_cause(self):
        self.write({'state': 'identified'})

    def action_start_actions(self):
        self.write({'state': 'actions'})

    def action_close(self):
        self.ensure_one()
        if self.open_actions:
            self.write({'state': 'closed'})
        else:
            self.write({'state': 'closed'})


class SfIncidentAction(models.Model):
    _name = 'sf.incident.action'
    _description = 'Incident Action'

    incident_id = fields.Many2one('sf.incident', string='Incident',
                                  required=True, ondelete='cascade')
    company_id = fields.Many2one(related='incident_id.company_id', store=True)
    action_type = fields.Selection([
        ('corrective', 'Corrective'), ('preventive', 'Preventive')],
        required=True, default='corrective')
    description = fields.Text(string='Action', required=True)
    owner_id = fields.Many2one('res.users', string='Owner', required=True)
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('open', 'Open'), ('done', 'Done'), ('cancelled', 'Cancelled')],
        default='open', tracking=True)
    completion_note = fields.Text(string='Completion Note')

    def action_done(self):
        self.write({'state': 'done'})
