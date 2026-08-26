import json
from odoo import api, fields, models


class AutomationLog(models.Model):
    _name = 'automation.log'
    _description = 'Automation Execution Log'
    _order = 'started_at desc'

    flow_id = fields.Many2one('automation.flow', string='Flow', required=True, ondelete='cascade')
    run_id = fields.Char(string='Run ID', required=True, copy=False, default=lambda s: s.env['ir.sequence'].next_by_code('automation.log.run') or 'RUN-%s' % s.env['ir.sequence'].next_by_code('automation.log.run'))

    # Execution context
    trigger = fields.Selection([
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
        ('scheduled', 'Scheduled'),
        ('webhook', 'Webhook'),
        ('test', 'Test Run'),
    ], string='Trigger', default='manual')

    triggered_by_id = fields.Many2one('res.users', string='Triggered By')
    test_mode = fields.Boolean(string='Test Mode', default=False)

    # Data
    input_data = fields.Text(string='Input Data (JSON)')
    output_data = fields.Text(string='Output Data (JSON)')

    # Status
    status = fields.Selection([
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='running')

    # Timing
    started_at = fields.Datetime(string='Started At', default=fields.Datetime.now)
    completed_at = fields.Datetime(string='Completed At')
    duration_ms = fields.Integer(string='Duration (ms)')

    # Error
    error_message = fields.Text(string='Error Message')
    error_node_id = fields.Many2one('automation.node', string='Failed Node')

    # Node execution details
    node_log_ids = fields.One2many('automation.node.log', 'log_id', string='Node Logs')

    def _compute_duration(self):
        for log in self:
            if log.started_at and log.completed_at:
                delta = log.completed_at - log.started_at
                log.duration_ms = int(delta.total_seconds() * 1000)


class AutomationNodeLog(models.Model):
    _name = 'automation.node.log'
    _description = 'Automation Node Execution Log'
    _order = 'started_at'

    log_id = fields.Many2one('automation.log', string='Execution Log', required=True, ondelete='cascade')
    flow_id = fields.Many2one(related='log_id.flow_id', string='Flow', store=True)
    node_id = fields.Many2one('automation.node', string='Node', required=True)
    node_type = fields.Selection(related='node_id.category', string='Node Type', store=True)

    # Execution
    status = fields.Selection([
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ], string='Status', default='pending')

    # Data
    input_data = fields.Text(string='Input Data (JSON)')
    output_data = fields.Text(string='Output Data (JSON)')

    # Timing
    started_at = fields.Datetime(string='Started At')
    completed_at = fields.Datetime(string='Completed At')
    duration_ms = fields.Integer(string='Duration (ms)')

    # Error
    error_message = fields.Text(string='Error Message')

    # Retry
    retry_count = fields.Integer(string='Retry Count', default=0)
    max_retries = fields.Integer(string='Max Retries', default=3)

    def _compute_duration(self):
        for nl in self:
            if nl.started_at and nl.completed_at:
                delta = nl.completed_at - nl.started_at
                nl.duration_ms = int(delta.total_seconds() * 1000)