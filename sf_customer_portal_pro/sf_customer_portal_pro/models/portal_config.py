from odoo import api, fields, models


class PortalConfig(models.Model):
    _name = 'portal.config'
    _description = 'Customer Portal Configuration'

    name = fields.Char(string='Portal Name', required=True, default='Customer Portal')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company)

    # Branding
    logo = fields.Binary(string='Logo', attachment=True)
    favicon = fields.Binary(string='Favicon', attachment=True)
    primary_color = fields.Char(string='Primary Color', default='#1f2937')
    secondary_color = fields.Char(string='Secondary Color', default='#3b82f6')
    custom_css = fields.Text(string='Custom CSS')

    # Domain
    custom_domain = fields.Char(string='Custom Domain', help='e.g., portal.mycompany.com')
    use_subdomain = fields.Boolean(string='Use Odoo Subdomain', default=True)
    subdomain = fields.Char(string='Subdomain', help='mycompany.odoo.com')

    # Features
    enable_payments = fields.Boolean(string='Enable Invoice Payments', default=True)
    enable_subscriptions = fields.Boolean(string='Enable Subscription Management', default=True)
    enable_returns = fields.Boolean(string='Enable Returns/RMA', default=True)
    enable_tickets = fields.Boolean(string='Enable Support Tickets', default=True)
    enable_documents = fields.Boolean(string='Enable Document Center', default=True)
    enable_knowledge_base = fields.Boolean(string='Enable Knowledge Base', default=True)

    # Payment providers
    payment_provider_ids = fields.Many2many('payment.provider', string='Enabled Payment Providers')

    # Authentication
    auth_method = fields.Selection([
        ('email', 'Email + Password'),
        ('oauth', 'OAuth2 (Google, Microsoft, etc.)'),
        ('saml', 'SAML 2.0'),
        ('magic_link', 'Magic Link'),
    ], string='Default Auth Method', default='email')
    allow_registration = fields.Boolean(string='Allow Self-Registration', default=True)
    require_verification = fields.Boolean(string='Require Email Verification', default=True)

    # Languages
    language_ids = fields.Many2many('res.lang', string='Available Languages')

    # Email templates
    welcome_template_id = fields.Many2one('mail.template', string='Welcome Email')
    invoice_notification_template_id = fields.Many2one('mail.template', string='Invoice Notification')
    ticket_notification_template_id = fields.Many2one('mail.template', string='Ticket Notification')

    def action_test_connection(self):
        return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {'title': 'Success', 'message': 'Portal config valid', 'type': 'success'}}