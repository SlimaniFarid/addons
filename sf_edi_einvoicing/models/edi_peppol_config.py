from odoo import api, fields, models


class EDIPeppolConfig(models.Model):
    _name = 'edi.peppol.config'
    _description = 'Peppol Access Point Configuration'

    name = fields.Char(string='Configuration Name', required=True, default='Peppol Access Point')
    company_id = fields.Many2one('res.company', required=True, default=lambda s: s.env.company)

    # SMP (Service Metadata Publisher)
    smp_url = fields.Char(string='SMP URL', default='https://smp.peppol.eu/')
    smp_api_key = fields.Char(string='SMP API Key', groups='base.group_system')

    # Certificate
    certificate = fields.Binary(string='Certificate (PKCS#12)', attachment=True, groups='base.group_system')
    certificate_password = fields.Char(string='Certificate Password', groups='base.group_system')
    certificate_expiry = fields.Date(string='Expiry Date')

    # Participant
    participant_id = fields.Char(string='Participant ID (ISO 6523)', help='e.g., 0192:123456789')
    participant_scheme = fields.Char(string='Scheme', default='0192')

    # Settings
    auto_register = fields.Boolean(string='Auto-Register Participants', default=True)
    validate_inbound = fields.Boolean(string='Validate Inbound', default=True)
    sign_outbound = fields.Boolean(string='Sign Outbound', default=True)

    # Status
    is_active = fields.Boolean(string='Active', default=True)
    last_health_check = fields.Datetime(string='Last Health Check')

    def action_health_check(self):
        self.write({'last_health_check': fields.Datetime.now()})
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {'title': 'OK', 'message': 'Peppol AP reachable', 'type': 'success'}}

    def action_register_participant(self):
        # Register participant in SMP
        pass