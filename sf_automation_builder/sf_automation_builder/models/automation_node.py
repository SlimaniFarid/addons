from odoo import api, fields, models


class AutomationNodeType(models.Model):
    _name = 'automation.node.type'
    _description = 'Automation Node Type'
    _order = 'category, sequence'

    name = fields.Char(string='Type Name', required=True)
    code = fields.Char(string='Code', required=True)
    category = fields.Selection([
        ('trigger', 'Trigger'),
        ('action', 'Action'),
        ('logic', 'Logic'),
        ('transform', 'Transform'),
        ('integration', 'Integration'),
    ], string='Category', required=True)

    description = fields.Text(string='Description')
    icon = fields.Char(string='Icon (FontAwesome)', default='fa-cog')
    color = fields.Char(string='Color', default='#3b82f6')

    # Configuration schema (JSON Schema)
    config_schema = fields.Text(string='Config Schema (JSON)',
        help='JSON Schema for node configuration')
    input_schema = fields.Text(string='Input Schema (JSON)')
    output_schema = fields.Text(string='Output Schema (JSON)')

    # Code template for execution
    code_template = fields.Text(string='Code Template (Python)')

    # Built-in
    is_builtin = fields.Boolean(string='Built-in', default=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)


class AutomationNode(models.Model):
    _name = 'automation.node'
    _description = 'Automation Node Instance'
    _order = 'flow_id, sequence'

    flow_id = fields.Many2one('automation.flow', string='Flow', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    # Type
    node_type_id = fields.Many2one('automation.node.type', string='Node Type', required=True)
    category = fields.Selection(related='node_type_id.category', store=True)

    # Configuration
    name = fields.Char(string='Node Name', required=True)
    config = fields.Text(string='Configuration (JSON)')
    position_x = fields.Integer(string='Position X', default=0)
    position_y = fields.Integer(string='Position Y', default=0)

    # Connections (handled via edges in canvas_data)
    # But we can also store them here for querying
    input_node_ids = fields.Many2many('automation.node', 'automation_node_input_rel', 'node_id', 'input_node_id', string='Input Nodes')
    output_node_ids = fields.Many2many('automation.node', 'automation_node_output_rel', 'node_id', 'output_node_id', string='Output Nodes')

    # Variables
    variable_ids = fields.One2many('automation.variable', 'node_id', string='Variables')

    # Execution
    execution_order = fields.Integer(string='Execution Order', compute='_compute_execution_order')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ], string='Status', default='pending')

    @api.depends('flow_id')
    def _compute_execution_order(self):
        # Simplified - real implementation would do topological sort
        for node in self:
            node.execution_order = node.sequence


class AutomationEdge(models.Model):
    _name = 'automation.edge'
    _description = 'Automation Flow Edge (Connection)'

    flow_id = fields.Many2one('automation.flow', string='Flow', required=True, ondelete='cascade')
    source_node_id = fields.Many2one('automation.node', string='Source Node', required=True, ondelete='cascade')
    target_node_id = fields.Many2one('automation.node', string='Target Node', required=True, ondelete='cascade')
    source_handle = fields.Char(string='Source Handle')
    target_handle = fields.Char(string='Target Handle')
    edge_type = fields.Selection([
        ('default', 'Default'),
        ('conditional_true', 'If True'),
        ('conditional_false', 'If False'),
    ], string='Edge Type', default='default')