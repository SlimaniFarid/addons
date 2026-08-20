# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductRegulation(models.Model):
    _name = 'sf.product.regulation'
    _description = 'Product Regulation'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    code = fields.Char(string='Code', required=True)
    market = fields.Char(string='Market')
    description = fields.Text(string='Description')
    mandatory = fields.Boolean(string='Mandatory', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.product.regulation')
        return super().create(vals)


class ProductComplianceRequirement(models.Model):
    _name = 'sf.product.compliance.requirement'
    _description = 'Product Compliance Requirement'
    _order = 'product_id, regulation_id'

    name = fields.Char(string='Number', required=True, index=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 ondelete='restrict', index=True, required=True)
    regulation_id = fields.Many2one('sf.product.regulation',
                                    string='Regulation',
                                    ondelete='restrict', required=True)
    requirement = fields.Text(string='Requirement', required=True)
    evidence = fields.Char(string='Evidence')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('satisfied', 'Satisfied'),
        ('not_satisfied', 'Not Satisfied'),
    ], string='State', default='pending', required=True, tracking=True,
       index=True)
    compliance_date = fields.Date(string='Compliance date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.product.compliance.requirement')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_product_compliance.group_compliance_manager'):
            raise UserError(_('Only compliance managers can validate '
                              'requirements.'))

    def action_mark_satisfied(self):
        self.ensure_one()
        self._check_manager()
        self.write({'state': 'satisfied',
                    'compliance_date': fields.Date.today()})

    def action_mark_not_satisfied(self):
        self.ensure_one()
        self._check_manager()
        self.write({'state': 'not_satisfied'})


class ProductComplianceDossier(models.Model):
    _name = 'sf.product.compliance.dossier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Compliance Dossier'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 ondelete='restrict', index=True, required=True)
    regulation_id = fields.Many2one('sf.product.regulation',
                                    string='Regulation',
                                    ondelete='restrict', required=True)
    version = fields.Char(string='Version', default='1.0')
    summary = fields.Html(string='Summary')
    attachment_ids = fields.Many2many('ir.attachment', string='Documents')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non Compliant'),
    ], string='State', default='draft', required=True, tracking=True,
       index=True)
    validated_date = fields.Datetime(string='Validated on')
    validated_by = fields.Many2one('res.users', string='Validated by',
                                   ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.product.compliance.dossier')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_product_compliance.group_compliance_manager'):
            raise UserError(_('Only compliance managers can validate '
                              'dossiers.'))

    def _check_requirements(self):
        requirements = self.env['sf.product.compliance.requirement'].search([
            ('product_id', '=', self.product_id.id),
            ('regulation_id', '=', self.regulation_id.id),
        ])
        return requirements.filtered(lambda r: r.state != 'satisfied')

    def action_validate(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'draft':
            raise UserError(_('Only draft dossiers can be sent to review.'))
        self.state = 'in_review'

    def action_mark_compliant(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'in_review':
            raise UserError(_('Only dossiers in review can be marked '
                              'compliant.'))
        unsatisfied = self._check_requirements()
        if unsatisfied:
            raise UserError(_('All requirements for this product and '
                              'regulation must be satisfied before the '
                              'dossier can be marked compliant.'))
        self.write({'state': 'compliant',
                    'validated_date': fields.Datetime.now(),
                    'validated_by': self.env.user.id})

    def action_mark_non_compliant(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'in_review':
            raise UserError(_('Only dossiers in review can be marked '
                              'non compliant.'))
        self.write({'state': 'non_compliant',
                    'validated_date': fields.Datetime.now(),
                    'validated_by': self.env.user.id})


class ProductComplianceCertificate(models.Model):
    _name = 'sf.product.compliance.certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Compliance Certificate'
    _order = 'expiry_date'

    name = fields.Char(string='Number', required=True, index=True)
    certificate_number = fields.Char(string='Certificate number')
    product_id = fields.Many2one('product.product', string='Product',
                                 ondelete='restrict', index=True, required=True)
    issuer = fields.Char(string='Issuer')
    issue_date = fields.Date(string='Issue date')
    expiry_date = fields.Date(string='Expiry date', index=True)
    attachment = fields.Binary(string='Attachment')
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], string='State', default='active', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.product.compliance.certificate')
        return super().create(vals)

    def action_expire(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_product_compliance.group_compliance_manager'):
            raise UserError(_('Only compliance managers can expire '
                              'certificates.'))
        if self.state != 'active':
            raise UserError(_('Only active certificates can be expired.'))
        self.state = 'expired'

    def _check_certificate_expiry(self):
        companies = self.env['res.company'].search([])
        manager = self.env.ref('sf_product_compliance.group_compliance_manager')
        today = fields.Date.today()
        for company in companies:
            certs = self.with_company(company).search([
                ('state', '=', 'active'),
                ('expiry_date', '!=', False),
                ('company_id', '=', company.id),
            ])
            for cert in certs:
                alert_days = company.sf_compliance_alert_days
                user = manager.users[:1] if manager.users else self.env.user
                if cert.expiry_date < today:
                    cert.state = 'expired'
                    cert.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Certificate %s has expired') % cert.name,
                        user_id=user.id)
                elif cert.expiry_date <= today + timedelta(days=alert_days):
                    cert.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Certificate %s expires on %s')
                        % (cert.name, cert.expiry_date),
                        user_id=user.id)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sf_compliance_state = fields.Selection([
        ('no_data', 'No Data'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non Compliant'),
    ], string='Compliance status',
       compute='_compute_sf_compliance_state')
    sf_compliance_dossier_ids = fields.One2many(
        'sf.product.compliance.dossier', 'product_id',
        string='Compliance dossiers')
    sf_compliance_requirement_ids = fields.One2many(
        'sf.product.compliance.requirement', 'product_id',
        string='Compliance requirements')
    sf_compliance_certificate_ids = fields.One2many(
        'sf.product.compliance.certificate', 'product_id',
        string='Compliance certificates')

    @api.depends('sf_compliance_dossier_ids.state',
                 'sf_compliance_dossier_ids.regulation_id.mandatory')
    def _compute_sf_compliance_state(self):
        for product in self:
            dossiers = product.sf_compliance_dossier_ids
            if all(d.state == 'compliant' for d in dossiers
                   if d.regulation_id.mandatory):
                product.sf_compliance_state = 'compliant'
            else:
                product.sf_compliance_state = 'non_compliant'


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_compliance_state = fields.Selection([
        ('no_data', 'No Data'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non Compliant'),
    ], string='Compliance status',
       compute='_compute_sf_compliance_state')
    sf_compliance_dossier_ids = fields.Many2many(
        'sf.product.compliance.dossier',
        string='Compliance dossiers',
        compute='_compute_sf_compliance_dossier_ids')

    @api.depends('product_variant_ids.sf_compliance_dossier_ids.state',
                 'product_variant_ids.sf_compliance_dossier_ids.regulation_id.mandatory')
    def _compute_sf_compliance_state(self):
        for template in self:
            dossiers = template.sf_compliance_dossier_ids
            if all(d.state == 'compliant' for d in dossiers
                   if d.regulation_id.mandatory):
                template.sf_compliance_state = 'compliant'
            else:
                template.sf_compliance_state = 'non_compliant'

    @api.depends('product_variant_ids.sf_compliance_dossier_ids')
    def _compute_sf_compliance_dossier_ids(self):
        for template in self:
            template.sf_compliance_dossier_ids = (
                template.product_variant_ids.mapped(
                    'sf_compliance_dossier_ids'))