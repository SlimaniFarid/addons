from odoo import api, fields, models


class McpToken(models.Model):
    _name = 'mcp.token'
    _description = 'MCP API Token'

    name = fields.Char(string='Token Label', required=True)
    server_id = fields.Many2one('mcp.server', string='Server', required=True, ondelete='cascade')
    active = fields.Boolean(string='Active', default=True)
    token = fields.Char(string='Token Value', required=True)
    expires_on = fields.Date(string='Expiration Date')
    last_used_on = fields.Datetime(string='Last Used', readonly=True)
    use_count = fields.Integer(string='Usage Count', default=0, readonly=True)

    def action_rotate(self):
        for rec in self:
            rec.token = self.env['ir.actions.server']._generate_signing_token(
                '%s-%s' % (rec.name, rec.id))
