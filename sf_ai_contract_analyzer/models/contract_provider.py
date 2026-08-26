from odoo import _, api, fields, models


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

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'contract.alert'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiration_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiration_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'contract.alert'

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
