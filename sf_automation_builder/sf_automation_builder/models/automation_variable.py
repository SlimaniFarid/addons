from odoo import api, fields, models


class AutomationVariable(models.Model):
    _name = 'automation.variable'
    _description = 'Automation Flow Variable'
    _order = 'flow_id, name'

    flow_id = fields.Many2one('automation.flow', string='Flow', required=True, ondelete='cascade')
    node_id = fields.Many2one('automation.node', string='Node', ondelete='cascade')

    name = fields.Char(string='Variable Name', required=True)
    var_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('datetime', 'DateTime'),
        ('date', 'Date'),
    ], string='Type', required=True, default='string')

    # Scope
    scope = fields.Selection([
        ('global', 'Global (Flow-level)'),
        ('node', 'Node-local'),
        ('input', 'Flow Input'),
        ('output', 'Flow Output'),
    ], string='Scope', default='global')

    # Default value
    default_value = fields.Text(string='Default Value')
    default_json = fields.Text(string='Default JSON (for json type)')

    # Validation
    required = fields.Boolean(string='Required', default=False)
    description = fields.Text(string='Description')
    validation_regex = fields.Char(string='Validation Regex')
    allowed_values = fields.Text(string='Allowed Values (JSON array)')

    # Runtime value (not stored)
    runtime_value = fields.Text(string='Runtime Value')

    def get_default(self):
        self.ensure_one()
        if self.var_type == 'json':
            return self.default_json
        return self.default_value