from odoo import api, fields, models


class ContractObligation(models.Model):
    _name = 'contract.obligation'
    _description = 'Contract Obligation'
    _order = 'due_date, id'

    document_id = fields.Many2one('contract.document', string='Contract', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    title = fields.Char(string='Obligation Title', required=True)
    description = fields.Html(string='Description')

    obligation_type = fields.Selection([
        ('delivery', 'Delivery / Performance'),
        ('payment', 'Payment'),
        ('reporting', 'Reporting'),
        ('compliance', 'Compliance / Certification'),
        ('insurance', 'Insurance'),
        ('confidentiality', 'Confidentiality / NDA'),
        ('data_protection', 'Data Protection / GDPR'),
        ('sla', 'Service Level Agreement'),
        ('renewal', 'Renewal / Notice'),
        ('termination', 'Termination'),
        ('warranty', 'Warranty / Guarantee'),
        ('indemnity', 'Indemnity'),
        ('force_majeure', 'Force Majeure'),
        ('dispute', 'Dispute Resolution'),
        ('other', 'Other'),
    ], string='Type', required=True)

    # Party responsible
    responsible_party = fields.Selection([
        ('our', 'Our Company'),
        ('counterparty', 'Counterparty'),
        ('both', 'Both Parties'),
        ('third_party', 'Third Party'),
    ], string='Responsible Party', required=True)

    # Dates
    due_date = fields.Date(string='Due Date')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    frequency = fields.Selection([
        ('once', 'One-time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
        ('on_event', 'On Event'),
    ], string='Frequency', default='once')

    # Financial
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency')

    # Status
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', tracking=True)

    # Compliance
    compliance_standard = fields.Char(string='Compliance Standard')
    evidence = fields.Html(string='Evidence of Compliance')
    evidence_attachments = fields.Many2many('ir.attachment', string='Evidence Attachments')

    # Linked records
    linked_record = fields.Reference(
        selection='_selection_models',
        string='Linked Record',
    )

    @api.model
    def _selection_models(self):
        return [
            ('sale.order', 'Sale Order'),
            ('purchase.order', 'Purchase Order'),
            ('account.move', 'Invoice/Bill'),
            ('project.task', 'Project Task'),
            ('helpdesk.ticket', 'Helpdesk Ticket'),
        ]

    def action_mark_complete(self):
        self.write({'state': 'completed'})

    def action_mark_overdue(self):
        overdue = self.search([
            ('state', '=', 'pending'),
            ('due_date', '<', fields.Date.today()),
        ])
        overdue.write({'state': 'overdue'})


class ContractRiskFlag(models.Model):
    _name = 'contract.risk.flag'
    _description = 'Contract Risk Flag'
    _order = 'severity desc, id'

    document_id = fields.Many2one('contract.document', string='Document', required=True, ondelete='cascade')

    title = fields.Char(string='Risk Title', required=True)
    description = fields.Html(string='Description')
    category = fields.Selection([
        ('financial', 'Financial'),
        ('legal', 'Legal / Compliance'),
        ('operational', 'Operational'),
        ('reputational', 'Reputational'),
        ('renewal', 'Renewal / Termination'),
        ('data_privacy', 'Data Privacy'),
        ('liability', 'Liability / Indemnity'),
        ('ip', 'Intellectual Property'),
        ('other', 'Other'),
    ], string='Category', required=True)

    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', required=True, default='medium')

    clause_reference = fields.Char(string='Clause Reference')
    recommendation = fields.Html(string='Recommendation')

    # Auto-detected
    auto_detected = fields.Boolean(string='Auto-Detected by AI', default=True)
    confidence = fields.Float(string='Detection Confidence')

    status = fields.Selection([
        ('open', 'Open'),
        ('under_review', 'Under Review'),
        ('mitigated', 'Mitigated'),
        ('accepted', 'Risk Accepted'),
        ('resolved', 'Resolved'),
    ], string='Status', default='open', tracking=True)

    owner_id = fields.Many2one('res.users', string='Owner')
    resolution = fields.Html(string='Resolution')
    resolved_date = fields.Date(string='Resolved Date')