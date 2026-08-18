from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AutomationFlow(models.Model):
    _name = 'automation.flow'
    _description = 'Automation Flow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Flow Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)

    # Version control
    version = fields.Integer(string='Version', default=1, readonly=True)
    parent_flow_id = fields.Many2one('automation.flow', string='Parent Flow')
    child_flow_ids = fields.One2many('automation.flow', 'parent_flow_id', string='Versions')

    # Canvas data (JSON)
    canvas_data = fields.Text(string='Canvas Data (JSON)',
        help='React Flow compatible: nodes, edges, viewport')

    # Execution settings
    trigger_mode = fields.Selection([
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
        ('scheduled', 'Scheduled'),
        ('webhook', 'Webhook'),
    ], string='Trigger Mode', default='auto')

    # Execution config
    max_concurrent_runs = fields.Integer(string='Max Concurrent Runs', default=1)
    timeout_seconds = fields.Integer(string='Timeout (seconds)', default=300)
    retry_on_failure = fields.Boolean(string='Retry on Failure', default=True)
    max_retries = fields.Integer(string='Max Retries', default=3)

    # Access control
    owner_id = fields.Many2one('res.users', string='Owner', default=lambda s: s.env.user)
    allowed_group_ids = fields.Many2many('res.groups', string='Allowed Groups')
    is_public = fields.Boolean(string='Public (All Users)', default=False)

    # Stats
    run_count = fields.Integer(string='Total Runs', default=0, readonly=True)
    success_count = fields.Integer(string='Successful Runs', default=0, readonly=True)
    failure_count = fields.Integer(string='Failed Runs', default=0, readonly=True)
    last_run = fields.Datetime(string='Last Run', readonly=True)

    # Logs
    log_ids = fields.One2many('automation.log', 'flow_id', string='Execution Logs')

    @api.constrains('canvas_data')
    def _check_canvas_data(self):
        for flow in self:
            if flow.canvas_data:
                try:
                    import json
                    data = json.loads(flow.canvas_data)
                    if not isinstance(data, dict) or 'nodes' not in data or 'edges' not in data:
                        raise ValidationError('Canvas data must contain "nodes" and "edges" arrays.')
                except json.JSONDecodeError as e:
                    raise ValidationError(f'Invalid JSON in canvas data: {e}')

    def action_new_version(self):
        new_flow = self.copy({
            'name': f'{self.name} (v{self.version + 1})',
            'version': self.version + 1,
            'parent_flow_id': self.id,
            'active': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'automation.flow',
            'res_id': new_flow.id,
            'view_mode': 'form',
        }

    def action_publish(self):
        self.write({'active': True})
        # Deactivate other versions
        self.search([
            ('parent_flow_id', '=', self.parent_flow_id.id or self.id),
            ('id', '!=', self.id),
        ]).write({'active': False})

    def action_test_run(self):
        return self._execute(context={'test_mode': True})

    def _execute(self, context=None, input_data=None):
        # Create execution log
        log = self.env['automation.log'].create({
            'flow_id': self.id,
            'status': 'running',
            'input_data': json.dumps(input_data or {}),
            'started_at': fields.Datetime.now(),
        })
        try:
            # Execute flow (simplified)
            result = self._run_flow(input_data or {})
            log.write({
                'status': 'success',
                'output_data': json.dumps(result),
                'completed_at': fields.Datetime.now(),
            })
            self.write({
                'run_count': self.run_count + 1,
                'success_count': self.success_count + 1,
                'last_run': fields.Datetime.now(),
            })
            return result
        except Exception as e:
            _logger.exception('Flow execution failed')
            log.write({
                'status': 'failed',
                'error_message': str(e),
                'completed_at': fields.Datetime.now(),
            })
            self.write({
                'run_count': self.run_count + 1,
                'failure_count': self.failure_count + 1,
            })
            raise

    def _run_flow(self, input_data):
        # Simplified execution - in reality would use a workflow engine
        return {'status': 'completed', 'data': input_data}


class AutomationFlowTemplate(models.Model):
    _name = 'automation.flow.template'
    _description = 'Automation Flow Template'

    name = fields.Char(string='Template Name', required=True)
    description = fields.Text(string='Description')
    category = fields.Selection([
        ('sales', 'Sales'),
        ('purchase', 'Purchase'),
        ('inventory', 'Inventory'),
        ('accounting', 'Accounting'),
        ('hr', 'Human Resources'),
        ('marketing', 'Marketing'),
        ('general', 'General'),
    ], string='Category', required=True)
    canvas_data = fields.Text(string='Canvas Data (JSON)', required=True)
    preview_image = fields.Binary(string='Preview Image', attachment=True)
    is_active = fields.Boolean(default=True)