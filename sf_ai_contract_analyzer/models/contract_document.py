import json
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ContractDocument(models.Model):
    _name = 'contract.document'
    _description = 'Contract Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Contract Name', required=True)
    contract_type = fields.Selection([
        ('sales', 'Sales Contract'),
        ('purchase', 'Purchase Contract'),
        ('employment', 'Employment Contract'),
        ('lease', 'Lease Agreement'),
        ('service', 'Service Agreement'),
        ('nda', 'NDA / Confidentiality'),
        ('partnership', 'Partnership / JV'),
        ('other', 'Other'),
    ], string='Type', required=True)

    # Source
    attachment_id = fields.Many2one('ir.attachment', string='Source File', required=True, ondelete='cascade')
    file_format = fields.Selection([
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('txt', 'Plain Text'),
        ('image', 'Image (OCR)'),
    ], string='Format', compute='_compute_file_format')

    # Parties
    party_ids = fields.One2many('contract.party', 'document_id', string='Parties')
    our_party_id = fields.Many2one('contract.party', string='Our Party', compute='_compute_our_party')

    # Key dates
    effective_date = fields.Date(string='Effective Date')
    expiration_date = fields.Date(string='Expiration Date')
    auto_renewal = fields.Boolean(string='Auto-Renewal')
    renewal_period = fields.Char(string='Renewal Period')
    notice_period_days = fields.Integer(string='Notice Period (Days)')

    # Financial
    currency_id = fields.Many2one('res.currency', string='Currency')
    contract_value = fields.Monetary(string='Contract Value', currency_field='currency_id')
    payment_terms = fields.Text(string='Payment Terms')
    penalty_clauses = fields.Text(string='Penalty Clauses')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('pending_signature', 'Pending Signature'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ], string='Status', default='draft', tracking=True)

    # AI Processing
    provider_id = fields.Many2one('contract.provider', string='AI Provider')
    processed = fields.Boolean(string='Processed by AI', default=False)
    processing_state = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Completed'),
        ('error', 'Error'),
    ], string='Processing State', default='pending')
    processing_error = fields.Text(string='Processing Error')
    confidence_score = fields.Float(string='Overall Confidence')

    # Extracted data
    extracted_data = fields.Text(string='Raw Extracted Data (JSON)')
    obligation_ids = fields.One2many('contract.obligation', 'document_id', string='Obligations')
    alert_ids = fields.One2many('contract.alert', 'document_id', string='Alerts')

    # Risk assessment
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Risk Level', compute='_compute_risk_level', store=True)
    risk_flags = fields.One2many('contract.risk.flag', 'document_id', string='Risk Flags')

    # Links
    sale_order_id = fields.Many2one('sale.order', string='Linked Sale Order')
    purchase_order_id = fields.Many2one('purchase.order', string='Linked Purchase Order')
    hr_contract_id = fields.Many2one('hr.contract', string='Linked HR Contract')
    fleet_lease_id = fields.Many2one('fleet.vehicle.lease', string='Linked Lease')

    @api.depends('attachment_id.mimetype')
    def _compute_file_format(self):
        for doc in self:
            if doc.attachment_id:
                mime = doc.attachment_id.mimetype
                if 'pdf' in mime:
                    doc.file_format = 'pdf'
                elif 'word' in mime or 'openxml' in mime:
                    doc.file_format = 'docx'
                elif 'text' in mime:
                    doc.file_format = 'txt'
                elif 'image' in mime:
                    doc.file_format = 'image'
                else:
                    doc.file_format = 'pdf'
            else:
                doc.file_format = 'pdf'

    @api.depends('party_ids')
    def _compute_our_party(self):
        for doc in self:
            doc.our_party_id = doc.party_ids.filtered(lambda p: p.is_our_party)[:1]

    @api.depends('risk_flags.severity')
    def _compute_risk_level(self):
        for doc in self:
            if any(f.severity == 'critical' for f in doc.risk_flags):
                doc.risk_level = 'critical'
            elif any(f.severity == 'high' for f in doc.risk_flags):
                doc.risk_level = 'high'
            elif any(f.severity == 'medium' for f in doc.risk_flags):
                doc.risk_level = 'medium'
            else:
                doc.risk_level = 'low'

    def action_process(self):
        for doc in self.filtered(lambda d: d.processing_state in ('pending', 'error')):
            doc.processing_state = 'processing'
            try:
                doc._process_with_ai()
                doc.processing_state = 'done'
            except Exception as e:
                _logger.exception('Contract processing failed')
                doc.processing_state = 'error'
                doc.processing_error = str(e)

    def _process_with_ai(self):
        # Simplified AI processing
        self.write({
            'processed': True,
            'confidence_score': 0.88,
            'extracted_data': json.dumps({
                'parties': ['Party A', 'Party B'],
                'effective_date': '2024-01-01',
                'expiration_date': '2025-12-31',
                'value': 100000,
                'currency': 'EUR',
            }),
        })
        # Create obligations
        self.env['contract.obligation'].create([
            {
                'document_id': self.id,
                'title': 'Delivery Obligation',
                'description': 'Deliver goods per schedule',
                'obligation_type': 'delivery',
                'due_date': '2024-12-31',
            },
            {
                'document_id': self.id,
                'title': 'Payment Obligation',
                'description': 'Pay invoices within 30 days',
                'obligation_type': 'payment',
                'due_date': '2024-12-31',
            },
        ])
        # Create risk flags
        self.env['contract.risk.flag'].create({
            'document_id': self.id,
            'title': 'Auto-Renewal Without Notice',
            'description': 'Contract auto-renews without explicit notice period',
            'severity': 'high',
            'category': 'renewal',
        })


class ContractParty(models.Model):
    _name = 'contract.party'
    _description = 'Contract Party'

    document_id = fields.Many2one('contract.document', string='Document', required=True, ondelete='cascade')
    name = fields.Char(string='Party Name', required=True)
    role = fields.Selection([
        ('our', 'Our Company'),
        ('counterparty', 'Counterparty'),
        ('guarantor', 'Guarantor'),
        ('witness', 'Witness'),
    ], string='Role', required=True)
    is_our_party = fields.Boolean(string='Is Our Party')
    contact_name = fields.Char(string='Contact Person')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    legal_entity = fields.Char(string='Legal Entity')
    registration_number = fields.Char(string='Registration Number')
    vat = fields.Char(string='VAT Number')