import base64
import json
import logging
import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

DOC_TYPES = "invoice, contract, cv, claim, po, expense, other"


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
    api_key = fields.Char(string='API Key', required=True,
                          groups='base.group_system')
    model_name = fields.Char(string='Model Name')
    base_url = fields.Char(string='API Base URL')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    timeout = fields.Integer(string='Timeout (s)', default=60)

    # Capabilities
    supports_classification = fields.Boolean(default=True)
    supports_extraction = fields.Boolean(default=True)
    supports_ocr = fields.Boolean(default=True)

    document_ids = fields.One2many('docintel.document', 'provider_id',
                                   string='Documents')

    # ------------------------------------------------------------------ URLs
    def _get_url(self):
        self.ensure_one()
        if self.provider_type == 'mistral':
            return self.base_url or 'https://api.mistral.ai/v1/chat/completions'
        if self.provider_type == 'gemini':
            return (
                self.base_url
                or 'https://generativelanguage.googleapis.com/v1beta/models/'
            ) + f'{self.model_name or "gemini-1.5-flash"}:generateContent'
        if self.provider_type == 'claude':
            return self.base_url or 'https://api.anthropic.com/v1/messages'
        if self.provider_type == 'openai':
            return self.base_url or 'https://api.openai.com/v1/chat/completions'
        raise UserError(_('Unsupported provider type.'))

    def _headers(self):
        self.ensure_one()
        if self.provider_type == 'claude':
            return {
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
                'Content-Type': 'application/json',
            }
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    @staticmethod
    def _prompt():
        return f"""Classify this document and extract its key fields.
Answer with ONLY a valid JSON object, no markdown fence:
{{
  "document_type": one of {DOC_TYPES},
  "confidence": 0.0-1.0,
  "extracted_data": {{ free-form dict of the most relevant fields,
     e.g. for invoice: vendor_name, invoice_number, invoice_date,
     total_amount; for cv: full_name, email, skills[] }}
}}
If a field is not found use null."""

    # ------------------------------------------------------------- providers
    def _content_parts(self, b64, mime):
        return [
            {'type': 'text', 'text': self._prompt()},
            {'type': 'image_url',
             'image_url': f'data:{mime};base64,{b64}'},
        ]

    def _call_mistral(self, b64, mime):
        payload = {
            'model': self.model_name or 'pixtral-12b',
            'messages': [{'role': 'user',
                          'content': self._content_parts(b64, mime)}],
        }
        r = requests.post(self._get_url(), headers=self._headers(),
                          json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']

    def _call_openai(self, b64, mime):
        payload = {
            'model': self.model_name or 'gpt-4o-mini',
            'messages': [{'role': 'user',
                          'content': self._content_parts(b64, mime)}],
        }
        r = requests.post(self._get_url(), headers=self._headers(),
                          json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']

    def _call_gemini(self, b64, mime):
        payload = {
            'contents': [{'parts': [
                {'text': self._prompt()},
                {'inline_data': {'mime_type': mime, 'data': b64}},
            ]}],
        }
        r = requests.post(self._get_url(), headers=self._headers(),
                          json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()['candidates'][0]['content']['parts'][0]['text']

    def _call_claude(self, b64, mime):
        payload = {
            'model': self.model_name or 'claude-3-sonnet-20240229',
            'max_tokens': 2000,
            'messages': [{'role': 'user', 'content': [
                {'type': 'text', 'text': self._prompt()},
                {'type': 'image',
                 'source': {'type': 'base64', 'media_type': mime,
                            'data': b64}},
            ]}],
        }
        r = requests.post(self._get_url(), headers=self._headers(),
                          json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()['content'][0]['text']

    # -------------------------------------------------------------- dispatch
    def extract_document(self, file_data, filename, mime_type):
        """Call the configured AI provider. Returns parsed dict:
        {document_type, confidence, extracted_data{}}."""
        self.ensure_one()
        b64 = base64.b64encode(file_data or b'').decode()
        mime = mime_type or 'application/pdf'
        dispatch = {
            'mistral': self._call_mistral,
            'gemini': self._call_gemini,
            'claude': self._call_claude,
            'openai': self._call_openai,
        }
        fn = dispatch.get(self.provider_type)
        if not fn:
            raise UserError(_('Unsupported provider type.'))
        raw = fn(b64, mime)
        # strip accidental markdown fences / prose around JSON
        cleaned = raw.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('```')[1]
            if cleaned.startswith('json'):
                cleaned = cleaned[4:]
        start, end = cleaned.find('{'), cleaned.rfind('}')
        if start == -1 or end == -1:
            raise UserError(_('AI answer did not contain JSON.'))
        data = json.loads(cleaned[start:end + 1])
        doc_type = data.get('document_type') or 'other'
        allowed = {k for k, _ in self.env['docintel.document']
                   ._fields['document_type'].selection}
        if doc_type not in allowed:
            doc_type = 'other'
        try:
            confidence = float(data.get('confidence') or 0.0)
        except (TypeError, ValueError):
            confidence = 0.0
        return {
            'document_type': doc_type,
            'confidence': min(max(confidence, 0.0), 1.0),
            'extracted_data': data.get('extracted_data') or {},
        }


class DocIntelDocument(models.Model):
    _name = 'docintel.document'
    _description = 'Document for AI Processing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Document Name', required=True)
    provider_id = fields.Many2one('docintel.provider', string='AI Provider',
                                  required=True)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment',
                                    required=True, ondelete='cascade')

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
    extracted_fields = fields.One2many('docintel.extraction', 'document_id',
                                       string='Extracted Fields')

    # Routing
    target_model = fields.Char(string='Target Model', readonly=True)
    target_record_id = fields.Integer(string='Target Record ID',
                                      readonly=True)
    routing_rule_id = fields.Many2one('docintel.routing.rule',
                                      string='Applied Routing Rule')

    error_message = fields.Text(string='Error', readonly=True)

    def action_process(self):
        for doc in self.filtered(lambda d: d.state in
                                 ('draft', 'error', 'queued')):
            doc.state = 'processing'
            try:
                att = doc.attachment_id
                if not att:
                    raise UserError(_('No attachment'))
                file_data = base64.b64decode(att.datas)
                result = doc.provider_id.extract_document(
                    file_data, att.name, att.mimetype)
                doc.write({
                    'document_type': result.get('document_type', 'other'),
                    'confidence': result.get('confidence', 0.0),
                    'extracted_data': json.dumps(
                        result.get('extracted_data', {}), indent=2),
                    'state': ('review'
                              if result.get('confidence', 0) < 0.85
                              else 'done'),
                })
                doc._sync_extraction_lines(result.get('extracted_data', {}))
                doc._apply_routing()
            except Exception as e:
                _logger.exception('Processing failed')
                doc.write({'state': 'error', 'error_message': str(e)})

    def _sync_extraction_lines(self, data):
        """Mirror top-level scalar entries into extraction lines."""
        self.ensure_one()
        self.extracted_fields.unlink()
        vals = []
        seq = 10
        for k, v in (data or {}).items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            vals.append({
                'document_id': self.id,
                'sequence': seq,
                'field_name': k,
                'field_value': str(v) if v is not None else '',
            })
            seq += 5
        if vals:
            self.env['docintel.extraction'].create(vals)

    def _apply_routing(self):
        """Route classified documents to an Odoo model when that model is
        actually installed. Invoices additionally get a draft vendor bill
        built from extracted_data when enough info is present."""
        self.ensure_one()
        routes = {
            'invoice': 'account.move',
            'contract': 'contract.document',
            'cv': 'hr.applicant',
            'claim': 'helpdesk.ticket',
        }
        target_model = routes.get(self.document_type)
        if not target_model or target_model not in self.env:
            # target app not installed: keep classification only
            self.write({'state': 'done'})
            return
        self.target_model = target_model
        record_id = False
        try:
            data = json.loads(self.extracted_data or '{}')
        except ValueError:
            data = {}
        if self.document_type == 'invoice':
            record_id = self._route_invoice(data)
        self.target_record_id = record_id or 0
        self.write({'state': 'done'})

    def _route_invoice(self, data):
        """Create a draft vendor bill from extracted invoice data."""
        if not isinstance(data, dict) or not data.get('vendor_name'):
            return False
        partner = self.env['res.partner'].search([
            '|', ('name', '=ilike', data.get('vendor_name')),
            ('vat', '=', data.get('vendor_vat') or ''),
        ], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({
                'name': data.get('vendor_name'),
                'vat': data.get('vendor_vat') or None,
            })
        currency = self.env['res.currency'].search(
            [('name', '=', (data.get('currency') or 'EUR'))], limit=1)
        move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'ref': data.get('invoice_number') or self.name,
            'invoice_date': data.get('invoice_date') or None,
            'currency_id': currency.id or False,
        })
        return move.id


class DocIntelQueue(models.Model):
    _name = 'docintel.queue'
    _description = 'Document Processing Queue'
    _order = 'create_date desc'

    document_id = fields.Many2one('docintel.document', string='Document',
                                  required=True, ondelete='cascade')
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

    document_id = fields.Many2one('docintel.document', string='Document',
                                  required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    field_name = fields.Char(string='Field', required=True)
    field_value = fields.Char(string='Value')


class DocIntelRoutingRule(models.Model):
    _name = 'docintel.routing.rule'
    _description = 'Document Intelligence Routing Rule'
    _order = 'sequence'

    sequence = fields.Integer(default=10)
    name = fields.Char(string='Rule Name', required=True)
    domain_hint = fields.Char(string='Filename Contains')
    target_model = fields.Char(string='Target Model')
    active = fields.Boolean(default=True)

    def _find_matching(self, filename):
        """Return first active rule whose hint matches the filename."""
        for rule in self.search([('active', '=', True)],
                                order='sequence'):
            if rule.domain_hint and rule.domain_hint.lower() \
               in (filename or '').lower():
                return rule
        return self.env['docintel.routing.rule']
