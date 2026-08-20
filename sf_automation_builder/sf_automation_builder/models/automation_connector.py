from odoo import api, fields, models


class AutomationConnector(models.Model):
    _name = 'automation.connector'
    _description = 'Automation External Connector'
    _order = 'name'

    name = fields.Char(string='Connector Name', required=True)
    connector_type = fields.Selection([
        ('http', 'HTTP / REST API'),
        ('graphql', 'GraphQL'),
        ('soap', 'SOAP'),
        ('database', 'Database (SQL)'),
        ('ftp', 'FTP / SFTP'),
        ('email', 'Email (SMTP/IMAP)'),
        ('websocket', 'WebSocket'),
        ('mqtt', 'MQTT'),
    ], string='Type', required=True)

    # Configuration
    base_url = fields.Char(string='Base URL')
    auth_type = fields.Selection([
        ('none', 'None'),
        ('basic', 'Basic Auth'),
        ('bearer', 'Bearer Token'),
        ('api_key', 'API Key (Header)'),
        ('api_key_query', 'API Key (Query Param)'),
        ('oauth2', 'OAuth 2.0'),
        ('aws_sigv4', 'AWS Signature v4'),
    ], string='Authentication', default='none')

    # Auth fields (conditional)
    username = fields.Char(string='Username')
    password = fields.Char(string='Password', groups='base.group_system')
    bearer_token = fields.Char(string='Bearer Token', groups='base.group_system')
    api_key = fields.Char(string='API Key', groups='base.group_system')
    api_key_name = fields.Char(string='API Key Header/Param Name', default='Authorization')
    oauth2_client_id = fields.Char(string='OAuth2 Client ID')
    oauth2_client_secret = fields.Char(string='OAuth2 Client Secret', groups='base.group_system')
    oauth2_token_url = fields.Char(string='OAuth2 Token URL')
    oauth2_scope = fields.Char(string='OAuth2 Scope')

    # Request defaults
    default_headers = fields.Text(string='Default Headers (JSON)')
    timeout = fields.Integer(string='Timeout (seconds)', default=30)
    verify_ssl = fields.Boolean(string='Verify SSL', default=True)

    # Rate limiting
    rate_limit = fields.Integer(string='Rate Limit (req/min)', default=60)
    retry_on_failure = fields.Boolean(default=True)
    max_retries = fields.Integer(default=3)

    # Testing
    test_endpoint = fields.Char(string='Test Endpoint')
    test_method = fields.Selection([
        ('GET', 'GET'),
        ('POST', 'POST'),
    ], string='Test Method', default='GET')

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    def action_test_connection(self):
        self.ensure_one()
        # Test the connection
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {'title': 'Test', 'message': 'Connection test not implemented in demo', 'type': 'info'}}

    def _get_auth_headers(self):
        self.ensure_one()
        headers = {}
        if self.auth_type == 'basic':
            import base64
            creds = f'{self.username}:{self.password}'.encode()
            headers['Authorization'] = f'Basic {base64.b64encode(creds).decode()}'
        elif self.auth_type == 'bearer':
            headers['Authorization'] = f'Bearer {self.bearer_token}'
        elif self.auth_type == 'api_key':
            headers[self.api_key_name] = self.api_key
        elif self.auth_type == 'api_key_query':
            # Handled in URL params
            pass
        # OAuth2 would need token refresh logic
        return headers