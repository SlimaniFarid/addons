from odoo import api, fields, models


class McpRequestLog(models.Model):
    _name = 'mcp.request.log'
    _description = 'MCP Request Log'
    _order = 'create_date desc'

    server_id = fields.Many2one('mcp.server', string='Server', required=True, ondelete='cascade')
    tool = fields.Char(string='Tool')
    model = fields.Char(string='Model')
    status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('forbidden', 'Forbidden'),
    ], string='Status', default='success')
    response_ms = fields.Integer(string='Response (ms)')
    params = fields.Text(string='Parameters', readonly=True)
    result = fields.Text(string='Result', readonly=True)

    @api.autovacuum
    def _clean_old_logs(self):
        self.search([('create_date', '<', fields.Datetime.now() - fields.Date.from_string('30 days'))]).unlink()