from odoo import api, fields, models


class QMSAudit(models.Model):
    _name = 'qms.audit'
    _description = 'Internal/External Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'planned_date desc'

    name = fields.Char(string='Audit Number', required=True, copy=False, default='New')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    audit_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External (Registrar)'),
        ('supplier', 'Supplier Audit'),
        ('process', 'Process Audit'),
        ('product', 'Product Audit'),
        ('system', 'System Audit'),
    ], string='Audit Type', required=True)

    standard = fields.Selection([
        ('iso9001', 'ISO 9001:2015'),
        ('iso14001', 'ISO 14001'),
        ('iso45001', 'ISO 45001'),
        ('iatf16949', 'IATF 16949'),
        ('other', 'Other'),
    ], string='Standard', default='iso9001')

    # Scope
    name_scope = fields.Char(string='Audit Name/Scope')
    departments = fields.Many2many('hr.department', string='Departments')
    processes = fields.Many2many('qms.process', string='Processes')
    clauses = fields.Many2many('qms.iso.clause', string='ISO Clauses')

    # Schedule
    planned_date = fields.Date(string='Planned Date')
    planned_end_date = fields.Date(string='Planned End Date')
    actual_date = fields.Date(string='Actual Date')
    actual_end_date = fields.Date(string='Actual End Date')

    # Team
    lead_auditor_id = fields.Many2one('res.users', string='Lead Auditor', required=True)
    auditor_ids = fields.Many2many('res.users', string='Auditors')
    auditee_ids = fields.Many2many('res.users', string='Auditees')

    # Status
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('reporting', 'Reporting'),
        ('follow_up', 'Follow-up'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', tracking=True)

    # Findings
    finding_ids = fields.One2many('qms.audit.finding', 'audit_id', string='Findings')
    nc_count = fields.Integer(string='Non-Conformities', compute='_compute_nc_count')
    obs_count = fields.Integer(string='Observations', compute='_compute_nc_count')
    opp_count = fields.Integer(string='Opportunities', compute='_compute_nc_count')

    # Report
    report = fields.Html(string='Audit Report')
    report_date = fields.Date(string='Report Date')
    report_approved = fields.Boolean(string='Report Approved')

    @api.depends('finding_ids.type')
    def _compute_nc_count(self):
        for audit in self:
            audit.nc_count = len(audit.finding_ids.filtered(lambda f: f.type == 'nc'))
            audit.obs_count = len(audit.finding_ids.filtered(lambda f: f.type == 'obs'))
            audit.opp_count = len(audit.finding_ids.filtered(lambda f: f.type == 'opp'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qms.audit') or 'AUD-%s' % self.env['ir.sequence'].next_by_code('qms.audit')
        return super().create(vals_list)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_report(self):
        self.write({'state': 'reporting'})

    def action_followup(self):
        self.write({'state': 'follow_up'})

    def action_close(self):
        self.write({'state': 'closed'})


class QMSAuditFinding(models.Model):
    _name = 'qms.audit.finding'
    _description = 'Audit Finding'

    audit_id = fields.Many2one('qms.audit', string='Audit', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    type = fields.Selection([
        ('nc', 'Non-Conformity'),
        ('obs', 'Observation'),
        ('opp', 'Opportunity for Improvement'),
        ('strength', 'Strength'),
    ], string='Type', required=True)

    clause = fields.Char(string='Clause Reference')
    description = fields.Html(string='Description', required=True)
    evidence = fields.Html(string='Evidence')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    due_date = fields.Date(string='Due Date')

    # For NCs - link to NC/CAPA
    nc_id = fields.Many2one('qms.nc', string='Linked NC')
    capa_required = fields.Boolean(string='CAPA Required', default=True)