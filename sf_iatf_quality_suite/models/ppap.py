# -*- coding: utf-8 -*-
"""PPAP Models - Production Part Approval Process (AIAG PPAP-4, 18 Elements)."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IATFPPAPSubmission(models.Model):
    """PPAP Submission Header - Levels 1-5, 18 Elements."""
    _name = 'iatf.ppap.submission'
    _description = 'PPAP Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='PPAP Number', required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True,
                                  domain=[('customer_rank', '>', 0)], tracking=True)
    product_id = fields.Many2one('product.product', string='Part', required=True, tracking=True)
    part_revision = fields.Char(string='Part Revision')
    drawing_number = fields.Char(string='Drawing Number')
    drawing_revision = fields.Char(string='Drawing Revision')
    # PPAP Level (1-5)
    level = fields.Selection([
        ('1', 'Level 1: PSW Only'),
        ('2', 'Level 2: PSW + Product Samples + Limited Data'),
        ('3', 'Level 3: PSW + Product Samples + Complete Data (Default)'),
        ('4', 'Level 4: PSW + Requirements Defined by Customer'),
        ('5', 'Level 5: PSW + Product Samples + Complete Data at Supplier Location'),
    ], string='Submission Level', default='3', required=True, tracking=True)
    # Dates
    submission_date = fields.Date(string='Submission Date', default=fields.Date.today, tracking=True)
    due_date = fields.Date(string='Customer Due Date')
    approval_date = fields.Date(string='Approval Date', readonly=True)
    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('preparing', 'Preparing Package'),
        ('submitted', 'Submitted to Customer'),
        ('customer_review', 'Under Customer Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ], string='Status', default='draft', tracking=True, copy=False)
    # Elements (18 standard AIAG PPAP-4)
    element_ids = fields.One2many('iatf.ppap.element', 'submission_id', string='PPAP Elements', copy=True)
    # PSW (Part Submission Warrant)
    psw_id = fields.Many2one('iatf.ppap.psw', string='Part Submission Warrant', ondelete='cascade')
    # Linked records
    apqp_project_id = fields.Many2one('iatf.apqp.project', string='APQP Project', ondelete='restrict')
    control_plan_id = fields.Many2one('iatf.control.plan', string='Production Control Plan', ondelete='restrict')
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('iatf.ppap.submission') or 'PPAP-%s' % self.env['ir.sequence'].next_by_code('iatf.ppap.submission')
        res = super().create(vals_list)
        res._create_standard_elements()
        return res

    def _create_standard_elements(self):
        """Create the 18 standard AIAG PPAP-4 elements."""
        elements_def = [
            (1, 'Design Records', 'Ballooned drawings, specifications, material certs'),
            (2, 'Engineering Change Documents', 'ECN/ECR records if applicable'),
            (3, 'Customer Engineering Approval', 'Deviation requests, concession approvals'),
            (4, 'Design FMEA (DFMEA)', 'Link to DFMEA record'),
            (5, 'Process Flow Diagram', 'Link to PFD'),
            (6, 'Process FMEA (PFMEA)', 'Link to PFMEA record'),
            (7, 'Control Plan', 'Link to Production Control Plan'),
            (8, 'Measurement System Analysis (MSA)', 'Gauge R&R studies'),
            (9, 'Dimensional Results', 'Layout inspection results (up to 30 samples)'),
            (10, 'Material / Performance Test Results', 'Material certs, functional test results'),
            (11, 'Initial Process Studies (Cp, Cpk, Pp, Ppk)', 'Process capability studies'),
            (12, 'Qualified Laboratory Documentation', 'Lab accreditation, calibration certs'),
            (13, 'Appearance Approval Report (AAR)', 'Color, texture, visual standards'),
            (14, 'Sample Production Parts', 'Master sample, retain samples'),
            (15, 'Master Sample', 'Signed master sample'),
            (16, 'Checking Aids', 'Gauges, fixtures, calibration records'),
            (17, 'Customer-Specific Requirements', 'Customer-specific forms, checklists'),
            (18, 'Part Submission Warrant (PSW)', 'Summary document - auto-generated'),
        ]
        vals_list = []
        for num, name, desc in elements_def:
            required = self._is_element_required(num)
            vals_list.append({
                'submission_id': self.id,
                'element_number': num,
                'name': name,
                'description': desc,
                'required': required,
                'status': 'pending' if required else 'na',
            })
        self.env['iatf.ppap.element'].create(vals_list)
        # Create PSW
        self.env['iatf.ppap.psw'].create({'submission_id': self.id})

    def _is_element_required(self, element_number):
        """Determine if element is required based on PPAP level."""
        level = self.level
        if level == '1':
            return element_number == 18  # PSW only
        elif level == '2':
            return element_number in (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18)
        elif level == '3':
            return True  # All elements
        elif level == '4':
            # Customer-defined - default to all, user can set N/A
            return True
        elif level == '5':
            return True  # All elements at supplier location
        return True

    def action_prepare(self):
        self.write({'state': 'preparing'})

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_customer_review(self):
        self.write({'state': 'customer_review'})

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approval_date': fields.Date.today(),
        })

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_withdraw(self):
        self.write({'state': 'withdrawn'})

    def action_generate_package(self):
        """Generate complete PPAP package as PDF."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'iatf.ppap.package.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_submission_id': self.id},
        }


class IATFPPAPElement(models.Model):
    """PPAP Element - One of the 18 AIAG PPAP-4 elements."""
    _name = 'iatf.ppap.element'
    _description = 'PPAP Element'
    _order = 'element_number'

    submission_id = fields.Many2one('iatf.ppap.submission', string='PPAP Submission', required=True, ondelete='cascade')
    element_number = fields.Integer(string='Element #', required=True)
    name = fields.Char(string='Element Name', required=True)
    description = fields.Text(string='Description')
    required = fields.Boolean(string='Required for this Level', default=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('na', 'Not Applicable'),
    ], string='Status', default='pending', tracking=True)
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    review_date = fields.Date(string='Review Date')
    comments = fields.Text(string='Review Comments')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments / Evidence')
    # Company
    company_id = fields.Many2one(related='submission_id.company_id', store=True)

    def action_start(self):
        self.write({'status': 'in_progress'})

    def action_submit(self):
        self.write({'status': 'submitted'})

    def action_approve(self):
        self.write({
            'status': 'approved',
            'reviewer_id': self.env.uid,
            'review_date': fields.Date.today(),
        })

    def action_reject(self):
        self.write({
            'status': 'rejected',
            'reviewer_id': self.env.uid,
            'review_date': fields.Date.today(),
        })

    def action_set_na(self):
        self.write({'status': 'na'})


class IATFPPAPPSW(models.Model):
    """Part Submission Warrant (PSW) - AIAG PPAP-4 Form."""
    _name = 'iatf.ppap.psw'
    _description = 'Part Submission Warrant (PSW)'
    _rec_name = 'submission_id'

    submission_id = fields.Many2one('iatf.ppap.submission', string='PPAP Submission', required=True, ondelete='cascade')
    # Customer info
    customer_name = fields.Char(string='Customer Name', related='submission_id.customer_id.name', store=True)
    customer_part_number = fields.Char(string='Customer Part Number')
    customer_po_number = fields.Char(string='Customer PO Number')
    # Supplier info
    supplier_name = fields.Char(string='Supplier Name', related='submission_id.company_id.name', store=True)
    supplier_code = fields.Char(string='Supplier Code')
    supplier_address = fields.Text(string='Supplier Address')
    # Part info
    part_number = fields.Char(string='Part Number', related='submission_id.product_id.default_code', store=True)
    part_name = fields.Char(string='Part Name', related='submission_id.product_id.name', store=True)
    part_revision = fields.Char(string='Part Revision', related='submission_id.part_revision', store=True)
    drawing_number = fields.Char(string='Drawing Number', related='submission_id.drawing_number', store=True)
    drawing_revision = fields.Char(string='Drawing Revision', related='submission_id.drawing_revision', store=True)
    # Submission info
    submission_level = fields.Selection(related='submission_id.level', string='Submission Level', store=True)
    submission_date = fields.Date(string='Submission Date', related='submission_id.submission_date', store=True)
    # PSW Declaration
    declaration = fields.Selection([
        ('full', 'The organization confirms all PPAP elements are complete and meet requirements'),
        ('partial', 'The organization confirms PPAP elements meet requirements with noted exceptions'),
        ('interim', 'Interim approval - pending completion of open items'),
    ], string='Declaration', required=True, default='full')
    authorized_signatory = fields.Char(string='Authorized Signatory')
    signatory_title = fields.Char(string='Title')
    signature_date = fields.Date(string='Signature Date', default=fields.Date.today)
    # Additional
    reason_for_submission = fields.Selection([
        ('initial', 'Initial Submission'),
        ('engineering_change', 'Engineering Change'),
        ('tooling_change', 'Tooling Change'),
        ('process_change', 'Process Change'),
        ('supplier_change', 'Supplier Change'),
        ('revalidation', 'Revalidation / Annual'),
        ('other', 'Other'),
    ], string='Reason for Submission', default='initial')
    explanation = fields.Text(string='Explanation / Comments')
    # Company
    company_id = fields.Many2one(related='submission_id.company_id', store=True)

    def action_sign(self):
        self.write({
            'authorized_signatory': self.env.user.name,
            'signatory_title': self.env.user.job_title or '',
            'signature_date': fields.Date.today(),
        })


class IATFPPAPPackageWizard(models.TransientModel):
    """Wizard to generate PPAP package PDF."""
    _name = 'iatf.ppap.package.wizard'
    _description = 'Generate PPAP Package'

    submission_id = fields.Many2one('iatf.ppap.submission', string='PPAP Submission', required=True)
    include_elements = fields.Many2many('iatf.ppap.element', string='Elements to Include',
                                        domain="[('submission_id', '=', submission_id)]")
    include_psw = fields.Boolean(string='Include PSW', default=True)
    include_cover_page = fields.Boolean(string='Include Cover Page', default=True)
    include_toc = fields.Boolean(string='Include Table of Contents', default=True)
    company_logo = fields.Binary(string='Company Logo', related='submission_id.company_id.logo')

    def action_generate(self):
        """Generate PDF report using QWeb."""
        self.ensure_one()
        return self.env.ref('sf_iatf_quality_suite.action_report_ppap_package').report_action(self.submission_id)