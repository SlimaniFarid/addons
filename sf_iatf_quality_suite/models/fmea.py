# -*- coding: utf-8 -*-
"""FMEA Models - AIAG-VDA compliant DFMEA & PFMEA with RPN calculation."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IATFFMEA(models.Model):
    """FMEA Header - Design (DFMEA) or Process (PFMEA)."""
    _name = 'iatf.fmea'
    _description = 'FMEA (DFMEA / PFMEA) - AIAG-VDA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='FMEA Number', required=True, copy=False, readonly=True, default='New')
    fmea_type = fields.Selection([
        ('dfmea', 'Design FMEA (DFMEA)'),
        ('pfmea', 'Process FMEA (PFMEA)'),
    ], string='FMEA Type', required=True, tracking=True)
    project_id = fields.Many2one('iatf.apqp.project', string='APQP Project', ondelete='restrict')
    product_id = fields.Many2one('product.product', string='Product', required=True, tracking=True)
    process_id = fields.Many2one('iatf.process', string='Process', ondelete='restrict',
                                 domain="[('product_id', '=', product_id)]")
    # Team
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True, tracking=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')
    # Scope & Boundary
    scope = fields.Html(string='Scope of Analysis')
    boundary_diagram = fields.Html(string='Boundary Diagram / P-Diagram')
    # Items
    item_ids = fields.One2many('iatf.fmea.item', 'fmea_id', string='FMEA Items', copy=True)
    # Status Workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('obsolete', 'Obsolete'),
    ], string='Status', default='draft', tracking=True, copy=False)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    approved_date = fields.Date(string='Approved Date', readonly=True, copy=False)
    revision = fields.Integer(string='Revision', default=1, copy=False)
    # Linked Control Plan (for PFMEA)
    control_plan_ids = fields.One2many('iatf.control.plan', 'pfmea_id', string='Linked Control Plans')
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                seq_code = 'iatf.fmea.dfmea' if vals.get('fmea_type') == 'dfmea' else 'iatf.fmea.pfmea'
                vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or 'FMEA-%s' % self.env['ir.sequence'].next_by_code('iatf.fmea')
        return super().create(vals_list)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_submit_review(self):
        self.write({'state': 'review'})

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by_id': self.env.uid,
            'approved_date': fields.Date.today(),
        })

    def action_activate(self):
        self.write({'state': 'active'})

    def action_obsolete(self):
        self.write({'state': 'obsolete'})

    def action_revise(self):
        self.ensure_one()
        new_fmea = self.copy({
            'name': 'New',
            'state': 'draft',
            'revision': self.revision + 1,
            'approved_by_id': False,
            'approved_date': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'iatf.fmea',
            'res_id': new_fmea.id,
            'view_mode': 'form',
            'target': 'current',
        }


class IATFFMEAItem(models.Model):
    """FMEA Line Item - Function, Failure Mode, Cause, Effect, Controls, Ratings, Actions."""
    _name = 'iatf.fmea.item'
    _description = 'FMEA Item'
    _order = 'sequence, id'

    fmea_id = fields.Many2one('iatf.fmea', string='FMEA', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    # Function / Process Step
    function = fields.Char(string='Function / Process Step', required=True)
    requirement = fields.Char(string='Requirement / Specification')

    # Failure Analysis
    failure_mode = fields.Char(string='Failure Mode', required=True)
    failure_cause = fields.Char(string='Failure Cause', required=True)
    failure_effect = fields.Char(string='Failure Effect', required=True)

    # Current Controls
    prevention_control = fields.Char(string='Prevention Control')
    detection_control = fields.Char(string='Detection Control')

    # Ratings 1-10 (AIAG-VDA)
    severity = fields.Integer(string='Severity (S)', required=True, default=1,
                              help='1 = No effect, 10 = Safety/Regulatory non-compliance')
    occurrence = fields.Integer(string='Occurrence (O)', required=True, default=1,
                                help='1 = Remote, 10 = Very high')
    detection = fields.Integer(string='Detection (D)', required=True, default=1,
                               help='1 = Almost certain, 10 = Absolute uncertainty')

    # RPN Calculation
    rpn = fields.Integer(string='RPN (S × O × D)', compute='_compute_rpn', store=True, readonly=True)
    rpn_class = fields.Selection([
        ('low', 'Low (1–50)'),
        ('medium', 'Medium (51–150)'),
        ('high', 'High (151–350)'),
        ('critical', 'Critical (351–1000)'),
    ], string='RPN Class', compute='_compute_rpn', store=True, readonly=True)

    # Recommended Actions
    recommended_action = fields.Text(string='Recommended Action')
    action_responsible_id = fields.Many2one('res.users', string='Action Responsible')
    action_due_date = fields.Date(string='Action Due Date')

    # Action Taken & Re-rating
    action_taken = fields.Text(string='Action Taken')
    action_completion_date = fields.Date(string='Action Completion Date')
    new_severity = fields.Integer(string='New S')
    new_occurrence = fields.Integer(string='New O')
    new_detection = fields.Integer(string='New D')
    new_rpn = fields.Integer(string='New RPN', compute='_compute_new_rpn', store=True, readonly=True)
    new_rpn_class = fields.Selection([
        ('low', 'Low (1–50)'),
        ('medium', 'Medium (51–150)'),
        ('high', 'High (151–350)'),
        ('critical', 'Critical (351–1000)'),
    ], string='New RPN Class', compute='_compute_new_rpn', store=True, readonly=True)

    # Link to Control Plan (for PFMEA high RPN items)
    cp_line_ids = fields.One2many('iatf.control.plan.line', 'fmea_item_id', string='Control Plan Lines')

    # Company (related)
    company_id = fields.Many2one(related='fmea_id.company_id', store=True)

    @api.constrains('severity', 'occurrence', 'detection')
    def _check_ratings(self):
        for item in self:
            for field_name in ('severity', 'occurrence', 'detection'):
                val = getattr(item, field_name)
                if not 1 <= val <= 10:
                    raise ValidationError(_('Rating %s must be between 1 and 10.') % field_name.upper())

    @api.depends('severity', 'occurrence', 'detection')
    def _compute_rpn(self):
        for item in self:
            item.rpn = item.severity * item.occurrence * item.detection
            if item.rpn <= 50:
                item.rpn_class = 'low'
            elif item.rpn <= 150:
                item.rpn_class = 'medium'
            elif item.rpn <= 350:
                item.rpn_class = 'high'
            else:
                item.rpn_class = 'critical'

    @api.depends('new_severity', 'new_occurrence', 'new_detection')
    def _compute_new_rpn(self):
        for item in self:
            if item.new_severity and item.new_occurrence and item.new_detection:
                item.new_rpn = item.new_severity * item.new_occurrence * item.new_detection
                if item.new_rpn <= 50:
                    item.new_rpn_class = 'low'
                elif item.new_rpn <= 150:
                    item.new_rpn_class = 'medium'
                elif item.new_rpn <= 350:
                    item.new_rpn_class = 'high'
                else:
                    item.new_rpn_class = 'critical'
            else:
                item.new_rpn = 0
                item.new_rpn_class = 'low'

    def action_generate_cp_line(self):
        """Generate Control Plan line from high RPN PFMEA item."""
        self.ensure_one()
        if self.fmea_id.fmea_type != 'pfmea':
            raise ValidationError(_('Control Plan lines can only be generated from PFMEA items.'))
        # This will be called from wizard with CP context
        pass


class IATFProcess(models.Model):
    """Process definition for PFMEA linkage."""
    _name = 'iatf.process'
    _description = 'Manufacturing Process'
    _order = 'name'

    name = fields.Char(string='Process Name', required=True)
    code = fields.Char(string='Process Code')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Html(string='Process Description')
    process_flow_diagram = fields.Binary(string='Process Flow Diagram', attachment=True)
    pfd_filename = fields.Char(string='PFD Filename')
    operation_ids = fields.One2many('iatf.process.operation', 'process_id', string='Operations')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)


class IATFProcessOperation(models.Model):
    """Process Operation for PFMEA and Control Plan linkage."""
    _name = 'iatf.process.operation'
    _description = 'Process Operation'
    _order = 'sequence, id'

    process_id = fields.Many2one('iatf.process', string='Process', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Operation Name', required=True)
    description = fields.Text(string='Operation Description')
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center')
    equipment_ids = fields.Many2many('maintenance.equipment', string='Equipment')
    # Control Plan linkage
    cp_line_ids = fields.One2many('iatf.control.plan.line', 'operation_id', string='Control Plan Lines')
    company_id = fields.Many2one(related='process_id.company_id', store=True)