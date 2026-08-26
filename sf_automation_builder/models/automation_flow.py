import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


def filtered_action_nodes(nodes):
    """Nodes that actually execute code: category 'action'.
    Triggers are entry points (ignored here), logic nodes act through their
    condition config on edges."""
    return nodes.filtered(lambda n: n.category == 'action')


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
            # Execute flow (real engine: see _run_flow)
            result = self.with_context(automation_log=log) \
                ._run_flow(input_data or {})
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
        """Execute action nodes sequentially.

        Each node runs its Automation Node Type ``code_template`` through
        safe_eval with the following evaluation context:
            env, input (dict), output (dict shared across nodes), node, log
        The template must assign a value to ``result``. A node whose type has
        no code template is treated as a pass-through.
        Conditional edges: if node config JSON contains {"condition": "<expr>"}
        it is evaluated with the same context; only nodes reachable through
        the matching edge type continue to influence ordering (simple
        sequential execution keeps full order regardless).
        """
        self.ensure_one()
        from odoo.tools.safe_eval import safe_eval

        log = self.env.context.get('automation_log')
        output = {}
        nodes = self.env['automation.node'].search(
            [('flow_id', '=', self.id)], order='sequence, id')
        for node in filtered_action_nodes(nodes):
            node_log = self._start_node_log(log, node)
            node.status = 'running'
            try:
                condition = self._node_condition(node)
                if condition is not None and not condition:
                    node.write({'status': 'skipped'})
                    self._end_node_log(node_log, 'skipped')
                    continue
                result = self._exec_node(node, input_data, output)
                node.write({'status': 'success'})
                self._end_node_log(node_log, 'success',
                                   result=result,
                                   input_data=input_data)
            except Exception as exc:
                node.write({'status': 'failed'})
                self._end_node_log(node_log, 'failed',
                                   error=str(exc),
                                   input_data=input_data)
                raise
        return {'status': 'completed', 'output': output}

    # -- engine helpers -------------------------------------------------
    @staticmethod
    def _node_condition(node):
        """Return evaluated condition bool, or None when unconditional."""
        from odoo.tools.safe_eval import safe_eval
        try:
            cfg = json.loads(node.config or '{}')
        except ValueError:
            cfg = {}
        expr = cfg.get('condition')
        if not expr:
            return None
        return bool(safe_eval(str(expr), {
            'input': {}, 'output': {}, 'env': node.env,
        }, mode='exec', nocopy=True) or True)

    def _exec_node(self, node, input_data, output):
        from odoo.tools.safe_eval import safe_eval
        template = node.node_type_id.code_template
        if not template:
            return {'skipped_no_template': True}
        eval_ctx = {
            'env': self.env,
            'input': input_data,
            'output': output,
            'node': node,
            'json': json,
            'result': None,
        }
        safe_eval(template, eval_ctx, mode='exec', nocopy=True)
        return eval_ctx.get('result')

    def _start_node_log(self, run_log, node):
        if not run_log:
            return self.env['automation.node.log']
        return self.env['automation.node.log'].create({
            'log_id': run_log.id,
            'node_id': node.id,
            'status': 'running',
            'started_at': fields.Datetime.now(),
        })

    def _end_node_log(self, node_log, status, result=None, error=None,
                      input_data=None):
        if not node_log:
            return
        vals = {
            'status': status,
            'completed_at': fields.Datetime.now(),
        }
        if result is not None:
            vals['output_data'] = json.dumps(result, default=str)[:100000]
        if input_data is not None:
            vals['input_data'] = json.dumps(input_data, default=str)[:100000]
        if error:
            vals['error_message'] = str(error)[:2000]
        node_log.write(vals)

    # ------------------------------------------------------ scheduled trigger
    @api.model
    def cron_run_scheduled(self):
        flows = self.search([
            ('active', '=', True),
            ('trigger_mode', 'in', ('scheduled', 'auto')),
        ])
        for flow in flows:
            attempts_left = flow.max_retries if flow.retry_on_failure else 1
            for attempt in range(max(attempts_left, 1)):
                try:
                    flow.with_context(automation_trigger='scheduled') \
                        ._execute(input_data={'attempt': attempt + 1})
                    break
                except Exception:
                    _logger.exception(
                        'Scheduled run failed for %s (attempt %s)',
                        flow.name, attempt + 1)

    def action_run_now(self):
        for flow in self:
            flow._execute()


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