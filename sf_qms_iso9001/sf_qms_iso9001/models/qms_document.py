from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QMSDocument(models.Model):
    _name = 'qms.document'
    _description = 'QMS Document Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code'

    name = fields.Char(string='Document Title', required=True)
    code = fields.Char(string='Document Code', required=True, copy=False)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    # Classification
    category = fields.Selection([
        ('manual', 'Quality Manual'),
        ('procedure', 'Procedure'),
        ('work_instruction', 'Work Instruction'),
        ('form', 'Form/Template'),
        ('record', 'Record'),
        ('external', 'External Document'),
        ('policy', 'Policy'),
    ], string='Category', required=True)

    # Version control
    version = fields.Char(string='Version', required=True, default='1.0')
    previous_version_id = fields.Many2one('qms.document', string='Previous Version')
    next_version_id = fields.Many2one('qms.document', string='Next Version', readonly=True)

    # Content
    content = fields.Html(string='Content')
    attachment_id = fields.Many2one('ir.attachment', string='Document File', ondelete='restrict')
    effective_date = fields.Date(string='Effective Date', default=fields.Date.today)
    review_date = fields.Date(string='Next Review Date')

    # Status workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('obsolete', 'Obsolete'),
    ], string='Status', default='draft', tracking=True)

    # Ownership
    author_id = fields.Many2one('res.users', string='Author', default=lambda s: s.env.user)
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    approver_id = fields.Many2one('res.users', string='Approver')
    owner_id = fields.Many2one('res.users', string='Document Owner', default=lambda s: s.env.user)

    # Distribution
    distribution_ids = fields.One2many('qms.document.distribution', 'document_id', string='Distribution List')

    # ISO clause reference
    iso_clause = fields.Char(string='ISO 9001 Clause', help='e.g., 7.5.3.2')

    @api.constrains('code', 'version', 'company_id')
    def _check_unique_code_version(self):
        for doc in self:
            if self.search_count([
                ('code', '=', doc.code),
                ('version', '=', doc.version),
                ('company_id', '=', doc.company_id.id),
                ('id', '!=', doc.id),
            ]):
                raise ValidationError('Document code and version must be unique per company.')

    def action_submit_review(self):
        self.write({'state': 'under_review'})

    def action_approve(self):
        self.write({'state': 'approved', 'approver_id': self.env.user.id})

    def action_publish(self):
        self.write({'state': 'published', 'effective_date': fields.Date.today()})
        # Notify distribution list
        for dist in self.distribution_ids:
            dist._notify()

    def action_obsolete(self):
        self.write({'state': 'obsolete'})


class QMSDocumentDistribution(models.Model):
    _name = 'qms.document.distribution'
    _description = 'Document Distribution List'

    document_id = fields.Many2one('qms.document', string='Document', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True)
    department_id = fields.Many2one('hr.department', string='Department')
    role = fields.Selection([
        ('reader', 'Reader'),
        ('trainer', 'Trainer'),
        ('approver', 'Approver'),
    ], string='Role', default='reader')
    acknowledged = fields.Boolean(string='Acknowledged', default=False)
    acknowledged_date = fields.Datetime(string='Acknowledged Date')

    def _notify(self):
        # Send notification to user
        pass


class QMSDocumentType(models.Model):
    _name = 'qms.document.type'
    _description = 'QMS Document Type'

    name = fields.Char(string='Type Name', required=True)
    code_prefix = fields.Char(string='Code Prefix', required=True)
    requires_approval = fields.Boolean(default=True)
    requires_review = fields.Boolean(default=True)
    review_frequency_months = fields.Integer(default=12)