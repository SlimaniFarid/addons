import base64
import json
import logging
import requests
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class AiProvider(models.Model):
    _name = 'ai.ocr.provider'
    _description = 'AI OCR Provider Configuration'
    _order = 'sequence'

    name = fields.Char(string='Provider Name', required=True)
    provider_type = fields.Selection([
        ('mistral', 'Mistral AI (Pixtral)'),
        ('gemini', 'Google Gemini Pro Vision'),
        ('claude', 'Anthropic Claude 3'),
    ], string='Provider', required=True)
    api_key = fields.Char(string='API Key', required=True, groups='base.group_system')
    model_name = fields.Char(string='Model Name', default='pixtral-12b')
    base_url = fields.Char(string='API Base URL')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    timeout = fields.Integer(string='Timeout (seconds)', default=60)
    max_tokens = fields.Integer(string='Max Tokens', default=2000)
    temperature = fields.Float(string='Temperature', default=0.1)

    def _get_headers(self):
        self.ensure_one()
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def _get_url(self):
        self.ensure_one()
        if self.provider_type == 'mistral':
            return self.base_url or 'https://api.mistral.ai/v1/chat/completions'
        if self.provider_type == 'gemini':
            return f'{self.base_url or "https://generativelanguage.googleapis.com/v1beta/models"}/{self.model_name}:generateContent'
        if self.provider_type == 'claude':
            return self.base_url or 'https://api.anthropic.com/v1/messages'
        return ''

    def extract_invoice(self, file_data, filename, mime_type):
        self.ensure_one()
        b64 = base64.b64encode(file_data).decode()
        prompt = self._build_prompt()

        if self.provider_type == 'mistral':
            return self._call_mistral(b64, mime_type, prompt)
        elif self.provider_type == 'gemini':
            return self._call_gemini(b64, mime_type, prompt)
        elif self.provider_type == 'claude':
            return self._call_claude(b64, mime_type, prompt)
        raise UserError('Unsupported provider')

    def _build_prompt(self):
        return """Extract invoice data as JSON with these fields:
{
  "vendor_name": "string",
  "vendor_vat": "string or null",
  "vendor_address": "string or null",
  "invoice_number": "string",
  "invoice_date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD or null",
  "currency": "EUR/USD/etc",
  "total_amount": 123.45,
  "subtotal": 100.00,
  "tax_amount": 23.45,
  "payment_method": "string or null",
  "line_items": [
    {"description": "string", "quantity": 1, "unit_price": 100.00, "tax_rate": 20.0, "total": 120.00}
  ],
  "confidence": 0.95
}
Only output valid JSON. If a field is not found, use null."""

    def _call_mistral(self, b64, mime, prompt):
        payload = {
            'model': self.model_name,
            'messages': [{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': f'data:{mime};base64,{b64}'},
                ],
            }],
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
        }
        r = requests.post(self._get_url(), headers=self._get_headers(), json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        content = data['choices'][0]['message']['content']
        return json.loads(content)

    def _call_gemini(self, b64, mime, prompt):
        payload = {
            'contents': [{
                'parts': [
                    {'text': prompt},
                    {'inline_data': {'mime_type': mime, 'data': b64}},
                ],
            }],
            'generationConfig': {'maxOutputTokens': self.max_tokens, 'temperature': self.temperature},
        }
        r = requests.post(self._get_url(), headers=self._get_headers(), json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        content = data['candidates'][0]['content']['parts'][0]['text']
        return json.loads(content)

    def _call_claude(self, b64, mime, prompt):
        payload = {
            'model': self.model_name or 'claude-3-sonnet-20240229',
            'max_tokens': self.max_tokens,
            'messages': [{
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image', 'source': {'type': 'base64', 'media_type': mime, 'data': b64}},
                ],
            }],
        }
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
        }
        r = requests.post(self._get_url(), headers=headers, json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        content = data['content'][0]['text']
        return json.loads(content)


class AiOcrRequest(models.Model):
    _name = 'ai.ocr.request'
    _description = 'AI OCR Request'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    provider_id = fields.Many2one('ai.ocr.provider', string='Provider', required=True)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', required=True, ondelete='cascade')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True)

    vendor_name = fields.Char(string='Vendor Name')
    vendor_vat = fields.Char(string='Vendor VAT')
    vendor_address = fields.Text(string='Vendor Address')
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    due_date = fields.Date(string='Due Date')
    currency = fields.Char(string='Currency')
    total_amount = fields.Float(string='Total Amount')
    subtotal = fields.Float(string='Subtotal')
    tax_amount = fields.Float(string='Tax Amount')
    payment_method = fields.Char(string='Payment Method')
    confidence = fields.Float(string='Confidence', default=0.0)

    line_ids = fields.One2many('ai.ocr.line', 'request_id', string='Line Items')
    error_message = fields.Text(string='Error')

    create_bill = fields.Boolean(string='Create Vendor Bill')
    create_expense = fields.Boolean(string='Create Expense')
    created_bill_id = fields.Many2one('account.move', string='Created Bill')
    created_expense_id = fields.Many2one('hr.expense', string='Created Expense')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('ai.ocr.request') or 'OCR-%s' % self.env['ir.sequence'].next_by_code('ai.ocr.request')
        return super().create(vals_list)

    def action_process(self):
        for req in self:
            req.state = 'processing'
            try:
                att = req.attachment_id
                if not att:
                    raise UserError('No attachment')
                file_data = base64.b64decode(att.datas)
                mime = att.mimetype or 'application/pdf'
                result = req.provider_id.extract_invoice(file_data, att.name, mime)
                req._fill_from_result(result)
                req.state = 'done'
                if req.create_bill:
                    req._create_vendor_bill()
                if req.create_expense:
                    req._create_expense()
            except Exception as e:
                _logger.exception('OCR failed')
                req.state = 'error'
                req.error_message = str(e)

    def _fill_from_result(self, data):
        self.write({
            'vendor_name': data.get('vendor_name'),
            'vendor_vat': data.get('vendor_vat'),
            'vendor_address': data.get('vendor_address'),
            'invoice_number': data.get('invoice_number'),
            'invoice_date': data.get('invoice_date'),
            'due_date': data.get('due_date'),
            'currency': data.get('currency'),
            'total_amount': data.get('total_amount', 0.0),
            'subtotal': data.get('subtotal', 0.0),
            'tax_amount': data.get('tax_amount', 0.0),
            'payment_method': data.get('payment_method'),
            'confidence': data.get('confidence', 0.0),
        })
        for line in data.get('line_items', []):
            self.env['ai.ocr.line'].create({
                'request_id': self.id,
                'description': line.get('description'),
                'quantity': line.get('quantity', 1),
                'unit_price': line.get('unit_price', 0.0),
                'tax_rate': line.get('tax_rate', 0.0),
                'total': line.get('total', 0.0),
            })

    def _create_vendor_bill(self):
        self.ensure_one()
        partner = self.env['res.partner'].search([
            '|', ('name', '=ilike', self.vendor_name), ('vat', '=', self.vendor_vat or '')
        ], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({
                'name': self.vendor_name or 'Unknown Vendor',
                'vat': self.vendor_vat,
                'street': self.vendor_address,
            })
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'invoice_date': self.invoice_date or fields.Date.today(),
            'invoice_date_due': self.due_date,
            'ref': self.invoice_number,
            'currency_id': self.env['res.currency'].search([('name', '=', self.currency or 'EUR')], limit=1).id,
        })
        expense_account = partner.property_account_expense_id \
            or self.env['ir.property']._get(
                'property_account_expense_categ_id', 'product.category')
        for line in self.line_ids:
            taxes = self.env['account.tax']
            if line.tax_rate:
                taxes = taxes.search([
                    ('type_tax_use', '=', 'purchase'),
                    ('amount_type', '=', 'percent'),
                    ('amount', '>=', line.tax_rate - 0.001),
                    ('amount', '<=', line.tax_rate + 0.001),
                ], limit=1)
            self.env['account.move.line'].create({
                'move_id': bill.id,
                'name': line.description,
                'account_id': expense_account.id,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
                'tax_ids': [(6, 0, taxes.ids)],
            })
        self.created_bill_id = bill.id

    def _create_expense(self):
        self.ensure_one()
        product = self.env['product.product'].search([
            ('can_be_expensed', '=', True)], limit=1)
        if not product:
            raise UserError(_(
                'No expensable product found. Create one to log OCR expenses.'))
        qty = line_qty = (self.line_ids and sum(self.line_ids.mapped('quantity'))) or 1.0
        unit = (self.total_amount / qty) if qty else self.total_amount
        exp = self.env['hr.expense'].create({
            'name': f'OCR: {self.invoice_number or self.name}',
            'product_id': product.id,
            'unit_amount': unit,
            'quantity': qty,
            'date': self.invoice_date or fields.Date.today(),
            'currency_id': self.env['res.currency'].search([('name', '=', self.currency or 'EUR')], limit=1).id,
        })
        self.created_expense_id = exp.id


class AiOcrLine(models.Model):
    _name = 'ai.ocr.line'
    _description = 'AI OCR Line Item'

    request_id = fields.Many2one('ai.ocr.request', string='Request', required=True, ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    tax_rate = fields.Float(string='Tax Rate %')
    total = fields.Float(string='Total')