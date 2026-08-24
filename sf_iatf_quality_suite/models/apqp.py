# -*- coding: utf-8 -*-
"""APQP Models - Advanced Product Quality Planning (AIAG 5 Phases, 23 Elements)."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IATFAPQPProject(models.Model):
    """APQP Project - 5 Phases with 23 standard elements."""
    _name = 'iatf.apqp.project'
    _description = 'APQP Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Project Name', required=True, tracking=True)
    project_number = fields.Char(string='Project Number', required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True,
                                  domain=[('customer_rank', '>', 0)], tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, tracking=True)
    product_revision = fields.Char(string='Product Revision')
    # Dates
    start_date = fields.Date(string='Project Start Date', default=fields.Date.today, tracking=True)
    target_sop_date = fields.Date(string='Target SOP Date', tracking=True)
    actual_sop_date = fields.Date(string='Actual SOP Date', readonly=True)
    # Current phase
    phase_current = fields.Selection([
        ('phase1', 'Phase 1: Plan & Define'),
        ('phase2', 'Phase 2: Product Design & Development'),
        ('phase3', 'Phase 3: Process Design & Development'),
        ('phase4', 'Phase 4: Product & Process Validation'),
        ('phase5', 'Phase 5: Production & Improvement'),
    ], string='Current Phase', default='phase1', tracking=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('phase1_complete', 'Phase 1 Complete'),
        ('phase2_complete', 'Phase 2 Complete'),
        ('phase3_complete', 'Phase 3 Complete'),
        ('phase4_complete', 'Phase 4 Complete'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], string='Project Status', default='draft', tracking=True, copy=False)
    # Team
    project_manager_id = fields.Many2one('res.users', string='Project Manager', required=True, tracking=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')
    # Elements (23 standard AIAG)
    element_ids = fields.One2many('iatf.apqp.element', 'project_id', string='APQP Elements', copy=True)
    # Linked records
    dfmea_id = fields.Many2one('iatf.fmea', string='Linked DFMEA', ondelete='restrict',
                               domain="[('fmea_type', '=', 'dfmea')]")
    pfmea_id = fields.Many2one('iatf.fmea', string='Linked PFMEA', ondelete='restrict',
                               domain="[('fmea_type', '=', 'pfmea')]")
    control_plan_ids = fields.One2many('iatf.control.plan', 'apqp_project_id', string='Control Plans')
    ppap_submission_id = fields.Many2one('iatf.ppap.submission', string='PPAP Submission', ondelete='restrict')
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('project_number', 'New') == 'New':
                vals['project_number'] = self.env['ir.sequence'].next_by_code('iatf.apqp.project') or 'APQP-%s' % self.env['ir.sequence'].next_by_code('iatf.apqp.project')
            # Auto-create 23 standard elements
            res = super().create(vals)
            res._create_standard_elements()
            return res

    def _create_standard_elements(self):
        """Create the 23 standard AIAG APQP elements."""
        elements_def = [
            # Phase 1: Plan & Define (1-4)
            ('phase1', 1, 'Voice of Customer (VOC) / Customer Input', 'Customer requirements, expectations, and inputs captured'),
            ('phase1', 2, 'Design Goals / Reliability Goals', 'Design targets, reliability, quality goals'),
            ('phase1', 3, 'Preliminary Process Flow Diagram', 'High-level process flow'),
            ('phase1', 4, 'Project Plan / Timing Plan', 'Milestones, resources, timing'),
            # Phase 2: Product Design & Development (5-11)
            ('phase2', 5, 'Design Review (DFMEA Input)', 'DFMEA initiation, design reviews'),
            ('phase2', 6, 'DFMEA', 'Design FMEA completion'),
            ('phase2', 7, 'Design for Manufacturing & Assembly (DFM/DFA)', 'Producibility analysis'),
            ('phase2', 8, 'Design Verification (DV) Plan & Results', 'Testing, simulation, validation plan'),
            ('phase2', 9, 'Prototype Control Plan', 'Prototype inspection plan'),
            ('phase2', 10, 'Engineering Drawings & Specifications', 'GD&T, material specs, drawings'),
            ('phase2', 11, 'Material & Equipment Specifications', 'Raw material, equipment specs'),
            # Phase 3: Process Design & Development (12-17)
            ('phase3', 12, 'Process Flow Diagram (PFD)', 'Detailed process flow'),
            ('phase3', 13, 'Process FMEA (PFMEA)', 'Process FMEA completion'),
            ('phase3', 14, 'Pre-Launch Control Plan', 'Pre-launch inspection plan'),
            ('phase3', 15, 'Measurement System Analysis (MSA) Plan', 'Gauge R&R planning'),
            ('phase3', 16, 'Packaging & Logistics Plan', 'Packaging, shipping, preservation'),
            ('phase3', 17, 'Process Instructions / Work Instructions', 'Standardized work, SOPs'),
            # Phase 4: Product & Process Validation (18-21)
            ('phase4', 18, 'Production Trial Run', 'Run @ rate, capability studies'),
            ('phase4', 19, 'Measurement System Analysis (MSA) Results', 'Gauge R&R execution & results'),
            ('phase4', 20, 'Pre-Production Control Plan', 'Pre-production inspection'),
            ('phase4', 21, 'Production Part Approval Process (PPAP)', 'PPAP submission'),
            # Phase 5: Production & Improvement (22-23)
            ('phase5', 22, 'Production Control Plan', 'Final production control plan'),
            ('phase5', 23, 'Lessons Learned / Continuous Improvement', 'Post-launch review, improvements'),
        ]
        vals_list = []
        for phase, num, name, desc in elements_def:
            vals_list.append({
                'project_id': self.id,
                'phase': phase,
                'element_number': num,
                'name': name,
                'description': desc,
                'status': 'not_started',
            })
        self.env['iatf.apqp.element'].create(vals_list)

    def action_start(self):
        self.write({'state': 'active'})

    def action_complete_phase(self):
        """Move to next phase based on current phase."""
        self.ensure_one()
        phase_map = {
            'phase1': ('phase2', 'phase1_complete'),
            'phase2': ('phase3', 'phase2_complete'),
            'phase3': ('phase4', 'phase3_complete'),
            'phase4': ('phase5', 'phase4_complete'),
            'phase5': (False, 'completed'),
        }
        next_phase, new_state = phase_map.get(self.phase_current, (False, False))
        if next_phase:
            # Check all elements in current phase are complete
            incomplete = self.element_ids.filtered(
                lambda e: e.phase == self.phase_current and e.status != 'complete'
            )
            if incomplete:
                raise ValidationError(_('All elements in current phase must be Complete before advancing.'))
            self.write({'phase_current': next_phase, 'state': new_state})
        else:
            self.write({'state': 'completed'})

    def action_close(self):
        self.write({'state': 'closed'})

    def _get_phase_progress(self, phase):
        """Compute completion % for a phase."""
        elements = self.element_ids.filtered(lambda e: e.phase == phase)
        if not elements:
            return 0.0
        complete = elements.filtered(lambda e: e.status == 'complete')
        return len(complete) / len(elements) * 100


class IATFAPQPElement(models.Model):
    """APQP Element - One of the 23 standard elements."""
    _name = 'iatf.apqp.element'
    _description = 'APQP Element'
    _order = 'phase, element_number'

    project_id = fields.Many2one('iatf.apqp.project', string='APQP Project', required=True, ondelete='cascade')
    phase = fields.Selection([
        ('phase1', 'Phase 1: Plan & Define'),
        ('phase2', 'Phase 2: Product Design & Development'),
        ('phase3', 'Phase 3: Process Design & Development'),
        ('phase4', 'Phase 4: Product & Process Validation'),
        ('phase5', 'Phase 5: Production & Improvement'),
    ], string='Phase', required=True)
    element_number = fields.Integer(string='Element #', required=True)
    name = fields.Char(string='Element Name', required=True)
    description = fields.Text(string='Description / Requirements')
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('complete', 'Complete'),
        ('na', 'N/A'),
    ], string='Status', default='not_started', tracking=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', tracking=True)
    due_date = fields.Date(string='Due Date', tracking=True)
    completion_date = fields.Date(string='Completion Date', readonly=True)
    # Evidence
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments / Evidence')
    # Linked records for traceability
    linked_dfmea_id = fields.Many2one('iatf.fmea', string='Linked DFMEA', ondelete='set null')
    linked_pfmea_id = fields.Many2one('iatf.fmea', string='Linked PFMEA', ondelete='set null')
    linked_cp_id = fields.Many2one('iatf.control.plan', string='Linked Control Plan', ondelete='set null')
    linked_ppap_id = fields.Many2one('iatf.ppap.submission', string='Linked PPAP', ondelete='set null')
    linked_msa_id = fields.Many2one('iatf.msa.study', string='Linked MSA Study', ondelete='set null')
    # Company
    company_id = fields.Many2one(related='project_id.company_id', store=True)

    def action_start(self):
        self.write({'status': 'in_progress'})

    def action_complete(self):
        self.write({
            'status': 'complete',
            'completion_date': fields.Date.today(),
        })

    def action_set_na(self):
        self.write({'status': 'na'})

    def action_reset(self):
        self.write({'status': 'not_started', 'completion_date': False})