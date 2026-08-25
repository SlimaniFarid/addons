import json
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DocIntelProvider(models.Model):
    _name = 'docintel.provider'
    _description = 'AI Document Intelligence Provider'
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
    timeout = fields.Integer(string='Timeout (s)', default=60)

    # Capabilities
    supports_classification = fields.Boolean(default=True)
    supports_extraction = fields.Boolean(default=True)
    supports_ocr = fields.Boolean(default=True)

    document_ids = fields.One2many('docintel.document', 'provider_id', string='Documents')

    def extract_document(self, file_data, filename, mime_type):
        self.ensure_one()
        # Simplified extraction - real impl would call API
        return {
            'document_type': 'invoice',
            'confidence': 0.92,
            'extracted_data': {
                'vendor_name': 'Sample Vendor',
                'invoice_number': 'INV-001',
                'invoice_date': '2024-01-15',
                'total_amount': 1250.00,
            }
        }


class DocIntelDocument(models.Model):
    _name = 'docintel.document'
    _description = 'Document for AI Processing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Document Name', required=True)
    provider_id = fields.Many2one('docintel.provider', string='AI Provider', required=True)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', required=True, ondelete='cascade')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('review', 'Needs Review'),
        ('done', 'Processed'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True)

    document_type = fields.Selection([
        ('invoice', 'Vendor Invoice'),
        ('contract', 'Contract'),
        ('cv', 'CV/Resume'),
        ('claim', 'Insurance Claim'),
        ('po', 'Purchase Order'),
        ('expense', 'Expense Receipt'),
        ('other', 'Other'),
    ], string='Document Type', readonly=True)

    confidence = fields.Float(string='Classification Confidence')
    extracted_data = fields.Text(string='Extracted Data (JSON)')
    extracted_fields = fields.One2many('docintel.extraction', 'document_id', string='Extracted Fields')

    # Routing
    target_model = fields.Char(string='Target Model', readonly=True)
    target_record_id = fields.Integer(string='Target Record ID', readonly=True)
    routing_rule_id = fields.Many2one('docintel.routing.rule', string='Applied Routing Rule')

    error_message = fields.Text(string='Error', readonly=True)

    def action_process(self):
        for doc in self.filtered(lambda d: d.state in ('draft', 'error', 'queued')):
            doc.state = 'processing'
            try:
                att = doc.attachment_id
                if not att:
                    raise UserError('No attachment')
                file_data = att.datas.decode('base64') if isinstance(att.datas, bytes) else base64.b64decode(att.datas)
                result = doc.provider_id.extract_document(file_data, att.name, att.mimetype)
                doc.write({
                    'document_type': result.get('document_type', 'other'),
                    'confidence': result.get('confidence', 0.0),
                    'extracted_data': json.dumps(result.get('extracted_data', {})),
                    'state': 'review' if result.get('confidence', 0) < 0.85 else 'done',
                })
                doc._apply_routing()
            except Exception as e:
                _logger.exception('Processing failed')
                doc.write({'state': 'error', 'error_message': str(e)})

    def _apply_routing(self):
        # Simplified routing logic
        routes = {
            'invoice': ('account.move', 'in_invoice'),
            'contract': ('contract.document', None),
            'cv': ('hr.applicant', None),
            'claim': ('helpdesk.ticket', None),
        }
        if self.document_type in routes:
            model, move_type = routes[self.document_type]
            self.target_model = model
            # In real impl: create draft record in target model
            self.write({'state': 'done'})


class DocIntelQueue(models.Model):
    _name = 'docintel.queue'
    _description = 'Document Processing Queue'
    _order = 'create_date desc'

    document_id = fields.Many2one('docintel.document', string='Document', required=True, ondelete='cascade')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ], string='Status', default='pending')
    attempts = fields.Integer(string='Attempts', default=0)
    error_message = fields.Text(string='Error')


class DocIntelExtraction(models.Model):
    _name = 'docintel.extraction'
    _description = 'Extracted Field'
    _order = 'sequence'

    document_id = fields.Many2one('docintel.document', string='Document', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    field_name = fields.Char(string='Field Name', required=True)
    field_value = fields.Char(string='Field Value')
    field_type = fields.Selection([
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('currency', 'Currency'),
        ('boolean', 'Boolean'),
    ], string='Field Type', default='text')
    confidence = fields.Float(string='Confidence')
    bbox = fields.Char(string='Bounding Box (JSON)')

class DocIntelRoutingRule(models.Model):
    _name = 'docintel.routing.rule'
    _description = 'Document Intelligence Routing Rule'
    _order = 'sequence'

    sequence = fields.Integer(default=10)
    name = fields.Char(string='Rule Name', required=True)
    domain_hint = fields.Char(string='Filename Contains')
    target_model = fields.Char(string='Target Model')
    active = fields.Boolean(default=True)
