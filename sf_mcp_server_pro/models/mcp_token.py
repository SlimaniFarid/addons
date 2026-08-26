from odoo import _, api, fields, models


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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'mcp.request.log'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
