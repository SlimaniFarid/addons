# -*- coding: utf-8 -*-
"""Control Plan Models - AIAG Control Plan with PFMEA linkage."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IATFControlPlan(models.Model):
    """Control Plan Header - Prototype, Pre-launch, Production phases."""
    _name = 'iatf.control.plan'
    _description = 'Control Plan (AIAG)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Control Plan Number', required=True, copy=False, readonly=True, default='New')
    product_id = fields.Many2one('product.product', string='Product', required=True, tracking=True)
    process_id = fields.Many2one('iatf.process', string='Process', ondelete='restrict')
    pfmea_id = fields.Many2one('iatf.fmea', string='Source PFMEA', ondelete='restrict',
                               domain="[('fmea_type', '=', 'pfmea')]")
    phase = fields.Selection([
        ('prototype', 'Prototype'),
        ('pre_launch', 'Pre-Launch'),
        ('production', 'Production'),
    ], string='Phase', required=True, default='prototype', tracking=True)
    version = fields.Integer(string='Version', default=1, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('obsolete', 'Obsolete'),
    ], string='Status', default='draft', tracking=True, copy=False)
    approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    approved_date = fields.Date(string='Approved Date', readonly=True, copy=False)
    effective_date = fields.Date(string='Effective Date')
    # Lines
    line_ids = fields.One2many('iatf.control.plan.line', 'control_plan_id', string='Control Plan Lines', copy=True)
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('iatf.control.plan') or 'CP-%s' % self.env['ir.sequence'].next_by_code('iatf.control.plan')
        return super().create(vals_list)

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
        # Create/update quality.points for active control plan
        self._sync_quality_points()

    def action_obsolete(self):
        self.write({'state': 'obsolete'})

    def action_revise(self):
        self.ensure_one()
        new_cp = self.copy({
            'name': 'New',
            'state': 'draft',
            'version': self.version + 1,
            'approved_by_id': False,
            'approved_date': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'iatf.control.plan',
            'res_id': new_cp.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_generate_from_pfmea(self):
        """Wizard to generate CP lines from linked PFMEA high-RPN items."""
        self.ensure_one()
        if not self.pfmea_id:
            raise ValidationError(_('No source PFMEA linked.'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'iatf.cp.generate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_control_plan_id': self.id},
        }

    def _sync_quality_points(self):
        """Create/update quality.point records from active Control Plan lines."""
        QualityPoint = self.env['quality.point']
        for line in self.line_ids.filtered(lambda l: l.quality_point_id):
            # Update existing
            line.quality_point_id.write({
                'name': line.name,
                'note': line.control_method,
                'normative_reference': line.specification,
            })
        for line in self.line_ids.filtered(lambda l: not l.quality_point_id and l.active_sync):
            # Create new
            point = QualityPoint.create({
                'name': line.name,
                'product_ids': [(6, 0, [line.control_plan_id.product_id.id])] if line.control_plan_id.product_id else [],
                'picking_type_ids': [(6, 0, line._get_picking_type_ids())],
                'operation_id': line.operation_id.workcenter_id.id if line.operation_id and line.operation_id.workcenter_id else False,
                'note': line.control_method,
                'normative_reference': line.specification,
                'test_type_id': line._get_test_type_id(),
            })
            line.write({'quality_point_id': point.id})


class IATFControlPlanLine(models.Model):
    """Control Plan Line - Product/Process characteristic with control method."""
    _name = 'iatf.control.plan.line'
    _description = 'Control Plan Line'
    _order = 'sequence, id'

    control_plan_id = fields.Many2one('iatf.control.plan', string='Control Plan', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    # Characteristic identification
    characteristic_type = fields.Selection([
        ('product', 'Product Characteristic'),
        ('process', 'Process Characteristic'),
    ], string='Characteristic Type', required=True)
    characteristic_name = fields.Char(string='Characteristic Name', required=True)
    characteristic_number = fields.Char(string='Characteristic No.')
    specification = fields.Char(string='Specification / Tolerance')
    spec_usl = fields.Float(string='USL (Upper Spec Limit)')
    spec_lsl = fields.Float(string='LSL (Lower Spec Limit)')
    spec_target = fields.Float(string='Target')

    # Control method
    control_method = fields.Selection([
        ('measurement', 'Measurement / Gauge'),
        ('visual', 'Visual Inspection'),
        ('go_nogo', 'Go / No-Go Gauge'),
        ('attribute', 'Attribute Count'),
        ('functional', 'Functional Test'),
        ('spc', 'SPC Chart'),
        ('other', 'Other'),
    ], string='Control Method', required=True)
    measurement_device = fields.Char(string='Measurement Device / Gauge')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    # MSA linkage
    msa_study_id = fields.Many2one('iatf.msa.study', string='MSA Study', ondelete='restrict',
                                   help='Gauge R&R study for this measurement method')

    # Sampling
    frequency = fields.Selection([
        ('each', 'Each Piece'),
        ('hourly', 'Hourly'),
        ('shift', 'Per Shift'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('lot', 'Per Lot'),
        ('setup', 'Per Setup'),
        ('custom', 'Custom'),
    ], string='Frequency', required=True)
    sample_size = fields.Integer(string='Sample Size', default=1)
    custom_frequency = fields.Char(string='Custom Frequency')

    # Reaction plan
    reaction_plan = fields.Text(string='Reaction Plan (Out of Control)')
    responsible_id = fields.Many2one('res.users', string='Responsible')

    # Link to PFMEA item (for traceability)
    fmea_item_id = fields.Many2one('iatf.fmea.item', string='Source PFMEA Item', ondelete='set null')
    # Link to process operation
    operation_id = fields.Many2one('iatf.process.operation', string='Operation', ondelete='restrict')

    # Odoo Quality integration
    quality_point_id = fields.Many2one('quality.point', string='Quality Point', ondelete='set null',
                                       help='Auto-created when Control Plan is activated')
    active_sync = fields.Boolean(string='Sync to Quality Points', default=True)

    # Company
    company_id = fields.Many2one(related='control_plan_id.company_id', store=True)

    def _get_picking_type_ids(self):
        """Get picking types for quality point creation based on operation."""
        self.ensure_one()
        if self.operation_id and self.operation_id.workcenter_id:
            return self.operation_id.workcenter_id.picking_type_ids.ids
        return self.env['stock.picking.type'].search([
            ('code', 'in', ['mrp_operation', 'internal', 'incoming'])
        ]).ids

    def _get_test_type_id(self):
        """Map control method to quality.test.type."""
        self.ensure_one()
        test_type_map = {
            'measurement': 'measure',
            'visual': 'passfail',
            'go_nogo': 'passfail',
            'attribute': 'measure',
            'functional': 'passfail',
            'spc': 'measure',
            'other': 'passfail',
        }
        test_type = self.env.ref('quality.test_type_%s' % test_type_map.get(self.control_method, 'passfail'), raise_if_not_found=False)
        return test_type.id if test_type else False


class IATFCPGenerateWizard(models.TransientModel):
    """Wizard to generate Control Plan lines from PFMEA items."""
    _name = 'iatf.cp.generate.wizard'
    _description = 'Generate Control Plan from PFMEA'

    control_plan_id = fields.Many2one('iatf.control.plan', string='Control Plan', required=True)
    pfmea_id = fields.Many2one(related='control_plan_id.pfmea_id', string='Source PFMEA')
    rpn_threshold = fields.Integer(string='RPN Threshold', default=150,
                                   help='Generate CP lines for PFMEA items with RPN >= threshold')
    include_items = fields.Many2many('iatf.fmea.item', string='PFMEA Items to Include',
                                     domain="[('fmea_id', '=', pfmea_id), ('rpn', '>=', rpn_threshold)]")

    def action_generate(self):
        self.ensure_one()
        cp = self.control_plan_id
        if not cp.pfmea_id:
            raise ValidationError(_('No PFMEA linked to this Control Plan.'))

        items = self.include_items or cp.pfmea_id.item_ids.filtered(lambda i: i.rpn >= self.rpn_threshold)
        if not items:
            raise ValidationError(_('No PFMEA items meet the RPN threshold.'))

        sequence = 10
        for item in items:
            cp.env['iatf.control.plan.line'].create({
                'control_plan_id': cp.id,
                'sequence': sequence,
                'characteristic_type': 'process',
                'characteristic_name': item.failure_mode,
                'specification': item.requirement or '',
                'control_method': 'measurement',
                'frequency': 'each',
                'sample_size': 1,
                'reaction_plan': item.action_taken or item.recommended_action or '',
                'responsible_id': item.action_responsible_id.id,
                'fmea_item_id': item.id,
                'operation_id': item._get_operation_id(),
            })
            sequence += 10

        return {'type': 'ir.actions.act_window_close'}

    def _get_operation_id(self):
        """Try to find matching operation from PFMEA function/step."""
        # Simplified - would need more logic in real implementation
        return False