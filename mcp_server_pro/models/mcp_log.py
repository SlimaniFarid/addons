from odoo import api, fields, models

class McpRequestLog(models.Model):
    _inherit = 'mcp.request.log'

    @api.autovacuum
    def _clean_old_logs(self):
        self.search([('create_date', '<', fields.Datetime.now() - fields.Date.from_string('30 days'))]).unlink()