from odoo import api, fields, models
from odoo.exceptions import ValidationError


class McpServer(models.Model):
    _name = 'mcp.server'
    _description = 'MCP Server'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('error', 'Error'),
    ], string='Status', default='draft', readonly=True, copy=False)

    base_url = fields.Char(
        string='Endpoint URL', compute='_compute_base_url', readonly=True)
    api_key = fields.Char(string='API Key', required=True, groups='base.group_system')
    allowed_models = fields.Char(
        string='Allowed Models',
        default='res.partner,res.users,sale.order,stock.move,account.move',
        help='Comma separated list of model names exposed to the AI assistant.',
    )
    max_requests_per_minute = fields.Integer(string='Max requests / minute', default=60)
    log_ids = fields.One2many('mcp.request.log', 'server_id', string='Request Logs')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The server code must be unique.'),
    ]

    @api.depends('code')
    def _compute_base_url(self):
        for rec in self:
            rec.base_url = '/mcp/%s' % rec.code

    @api.constrains('api_key')
    def _check_api_key(self):
        for rec in self:
            if len(rec.api_key) < 12:
                raise ValidationError('The API key must contain at least 12 characters.')

    def action_activate(self):
        self.state = 'ready'

    def action_reset(self):
        self.state = 'draft'

    def get_model_list(self):
        self.ensure_one()
        return [m.strip() for m in (self.allowed_models or '').split(',') if m.strip()]

    def is_model_allowed(self, model_name):
        self.ensure_one()
        return model_name in self.get_model_list()
