import requests
import json
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class WhatsAppAccount(models.Model):
    _name = 'whatsapp.account'
    _description = 'WhatsApp Business Account'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Account Name', required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Not Configured'),
        ('ready', 'Connected'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True, readonly=True)

    access_token = fields.Char(string='Access Token', required=True, groups='base.group_system')
    phone_number_id = fields.Char(string='Phone Number ID', required=True)
    business_account_id = fields.Char(string='Business Account ID')
    webhook_verify_token = fields.Char(string='Webhook Verify Token', groups='base.group_system')
    webhook_url = fields.Char(string='Webhook URL', readonly=True)
    api_version = fields.Char(string='API Version', default='v18.0')

    default_template_id = fields.Many2one('whatsapp.template', string='Default Template')
    message_ids = fields.One2many('whatsapp.message', 'account_id', string='Messages')
    template_ids = fields.One2many('whatsapp.template', 'account_id', string='Templates')

    _sql_constraints = [
        ('phone_id_uniq', 'unique(phone_number_id)', 'Phone Number ID must be unique.'),
    ]

    def action_test_connection(self):
        for acc in self:
            try:
                url = f'https://graph.facebook.com/{acc.api_version}/{acc.phone_number_id}'
                headers = {'Authorization': f'Bearer {acc.access_token}'}
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    acc.state = 'ready'
                else:
                    acc.state = 'error'
                    raise UserError(f'Connection failed: {resp.text}')
            except Exception as e:
                acc.state = 'error'
                raise UserError(f'Connection error: {e}')

    def action_fetch_templates(self):
        self.ensure_one()
        try:
            url = f'https://graph.facebook.com/{self.api_version}/{self.business_account_id or self.phone_number_id}/message_templates'
            headers = {'Authorization': f'Bearer {self.access_token}'}
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for tmpl in data.get('data', []):
                    existing = self.env['whatsapp.template'].search([
                        ('account_id', '=', self.id),
                        ('template_name', '=', tmpl.get('name')),
                    ], limit=1)
                    vals = {
                        'account_id': self.id,
                        'template_name': tmpl.get('name'),
                        'category': tmpl.get('category'),
                        'language': tmpl.get('language'),
                        'status': tmpl.get('status'),
                        'components': json.dumps(tmpl.get('components', [])),
                    }
                    if existing:
                        existing.write(vals)
                    else:
                        self.env['whatsapp.template'].create(vals)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {'title': 'Success', 'message': f'Fetched {len(data.get("data", []))} templates', 'type': 'success'},
                }
            else:
                raise UserError(f'Failed: {resp.text}')
        except Exception as e:
            raise UserError(f'Error: {e}')

    def send_message(self, to_number, template_name, language, components=None):
        self.ensure_one()
        url = f'https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'messaging_product': 'whatsapp',
            'to': to_number,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {'code': language},
            },
        }
        if components:
            payload['template']['components'] = components
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            return resp.json(), resp.status_code
        except Exception as e:
            _logger.exception('WhatsApp send failed')
            return {'error': str(e)}, 500


class WhatsAppTemplate(models.Model):
    _name = 'whatsapp.template'
    _description = 'WhatsApp Message Template'
    _order = 'name'

    name = fields.Char(string='Display Name', required=True)
    account_id = fields.Many2one('whatsapp.account', string='Account', required=True, ondelete='cascade')
    template_name = fields.Char(string='Template Name (Meta)', required=True)
    category = fields.Selection([
        ('marketing', 'Marketing'),
        ('utility', 'Utility'),
        ('authentication', 'Authentication'),
    ], string='Category', required=True)
    language = fields.Char(string='Language Code', default='en_US', required=True)
    status = fields.Selection([
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('paused', 'Paused'),
    ], string='Status', default='pending')
    components = fields.Text(string='Components (JSON)')
    header_type = fields.Selection([
        ('none', 'None'),
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ], string='Header Type', default='none')
    body_text = fields.Text(string='Body Text (for reference)')
    footer_text = fields.Text(string='Footer Text')
    button_count = fields.Integer(string='Buttons', default=0)

    _sql_constraints = [
        ('template_name_account_uniq', 'unique(template_name, account_id)', 'Template name must be unique per account.'),
    ]

    def get_components_list(self):
        try:
            return json.loads(self.components or '[]')
        except (json.JSONDecodeError, TypeError):
            return []

    def render_body(self, values):
        text = self.body_text or ''
        for key, val in (values or {}).items():
            text = text.replace(f'{{{{{key}}}}}', str(val))
        return text


class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'WhatsApp Message Log'
    _order = 'create_date desc'
    _rec_name = 'to_number'

    account_id = fields.Many2one('whatsapp.account', string='Account', required=True, ondelete='cascade')
    template_id = fields.Many2one('whatsapp.template', string='Template', ondelete='set null')
    to_number = fields.Char(string='To Number', required=True)
    to_name = fields.Char(string='Recipient Name')
    res_model = fields.Char(string='Related Model')
    res_id = fields.Integer(string='Related Record ID')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ], string='Status', default='draft', tracking=True)
    direction = fields.Selection([
        ('outbound', 'Outbound'),
        ('inbound', 'Inbound'),
    ], string='Direction', default='outbound')
    meta_message_id = fields.Char(string='Meta Message ID')
    error_message = fields.Text(string='Error')
    body_text = fields.Text(string='Rendered Body')
    components_sent = fields.Text(string='Components Sent')

    def action_send(self):
        for msg in self.filtered(lambda m: m.status in ('draft', 'failed', 'queued')):
            msg.status = 'queued'
            if not msg.template_id:
                raise UserError('Template required')
            to = msg.to_number
            components = []
            try:
                components = json.loads(msg.components_sent) if msg.components_sent else []
            except (json.JSONDecodeError, TypeError):
                pass
            result, code = msg.account_id.send_message(
                to, msg.template_id.template_name, msg.template_id.language, components)
            if code == 200:
                msg.status = 'sent'
                msg.meta_message_id = result.get('messages', [{}])[0].get('id')
            else:
                msg.status = 'failed'
                msg.error_message = str(result)

    def action_retry(self):
        self.filtered(lambda m: m.status == 'failed').write({'status': 'draft'}).action_send()