from odoo import api, fields, models


class ContractProvider(models.Model):
    _name = 'contract.provider'
    _description = 'AI Contract Analysis Provider'
    _order = 'sequence'

    name = fields.Char(string='Provider Name', required=True)
    provider_type = fields.Selection([
        ('mistral', 'Mistral AI'),
        ('gemini', 'Google Gemini'),
        ('claude', 'Anthropic Claude'),
        ('openai', 'OpenAI'),
    ], string='Provider', required=True)
    api_key = fields.Char(string='API Key', required=True, groups='base.group_system')
    model_name = fields.Char(string='Model Name')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    timeout = fields.Integer(string='Timeout (s)', default=120)
    max_tokens = fields.Integer(string='Max Tokens', default=4000)
    temperature = fields.Float(string='Temperature', default=0.1)

    # Capabilities
    supports_classification = fields.Boolean(default=True)
    supports_extraction = fields.Boolean(default=True)
    supports_risk_analysis = fields.Boolean(default=True)
    supports_multilang = fields.Boolean(default=True)

    def extract_contract(self, file_data, filename, mime_type):
        self.ensure_one()
        # Simplified extraction
        return {
            'parties': ['Party A', 'Party B'],
            'effective_date': '2024-01-01',
            'expiration_date': '2025-12-31',
            'auto_renewal': True,
            'renewal_period': '1 year',
            'notice_period_days': 30,
            'contract_value': 100000,
            'currency': 'EUR',
            'payment_terms': 'Net 30',
            'obligations': [
                {'title': 'Delivery', 'type': 'delivery', 'due_date': '2024-12-31'},
                {'title': 'Payment', 'type': 'payment', 'due_date': '2024-12-31'},
            ],
            'risk_flags': [
                {'title': 'Auto-Renewal', 'severity': 'high', 'category': 'renewal'},
            ],
        }