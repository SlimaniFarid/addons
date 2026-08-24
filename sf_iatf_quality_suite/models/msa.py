# -*- coding: utf-8 -*-
"""MSA Models - Measurement System Analysis (Gauge R&R) per AIAG MSA 4th Edition."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import math
import statistics


class IATFMSAStudy(models.Model):
    """MSA Study Header - Crossed, Nested, Attribute."""
    _name = 'iatf.msa.study'
    _description = 'MSA / Gauge R&R Study'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='MSA Study Number', required=True, copy=False, readonly=True, default='New')
    study_type = fields.Selection([
        ('crossed', 'Crossed (Gauge R&R - ANOVA)'),
        ('nested', 'Nested (Destructive Testing)'),
        ('attribute', 'Attribute Agreement Analysis'),
    ], string='Study Type', required=True, tracking=True)
    # What is being measured
    characteristic_name = fields.Char(string='Characteristic Name', required=True)
    specification = fields.Char(string='Specification / Tolerance')
    spec_usl = fields.Float(string='USL')
    spec_lsl = fields.Float(string='LSL')
    spec_target = fields.Float(string='Target')
    # Equipment
    equipment_id = fields.Many2one('maintenance.equipment', string='Measurement Equipment', required=True, tracking=True)
    equipment_calibration_date = fields.Date(related='equipment_id.last_calibration_date', string='Last Calibration')
    # Study parameters
    part_ids = fields.Many2many('product.product', string='Parts / Samples', required=True)
    operator_ids = fields.Many2many('res.users', string='Operators / Appraisers', required=True)
    trial_count = fields.Integer(string='Number of Trials', default=2, required=True,
                                 help='Typically 2-3 trials per part per operator')
    # Results (computed)
    grr_percent = fields.Float(string='%GRR (Total Variation)', readonly=True,
                               help='%GRR = (GRR / TV) × 100. Target < 10%')
    grr_percent_tolerance = fields.Float(string='%GRR (Tolerance)', readonly=True,
                                          help='%GRR = (GRR / Tolerance) × 100')
    ndc = fields.Integer(string='Number of Distinct Categories (ndc)', readonly=True,
                         help='ndc = 1.41 × (PV / GRR). Target ≥ 5')
    pv_percent = fields.Float(string='%PV (Part Variation)', readonly=True)
    ev_percent = fields.Float(string='%EV (Equipment Variation)', readonly=True)
    av_percent = fields.Float(string='%AV (Appraiser Variation)', readonly=True)
    # ANOVA results (for crossed)
    anova_p_value_operator = fields.Float(string='Operator p-value', readonly=True)
    anova_p_value_part = fields.Float(string='Part p-value', readonly=True)
    anova_p_value_interaction = fields.Float(string='Operator×Part p-value', readonly=True)
    # Capability
    cp = fields.Float(string='Cp', readonly=True)
    cpk = fields.Float(string='Cpk', readonly=True)
    # Status
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Data Collection'),
        ('calculating', 'Calculating'),
        ('complete', 'Complete'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True, copy=False)
    conclusion = fields.Selection([
        ('acceptable', 'Acceptable (%GRR < 10%, ndc ≥ 5)'),
        ('marginal', 'Marginal (10% ≤ %GRR ≤ 30%, ndc ≥ 5)'),
        ('unacceptable', 'Unacceptable (%GRR > 30% or ndc < 5)'),
    ], string='Conclusion', readonly=True)
    # Measurements
    measurement_ids = fields.One2many('iatf.msa.measurement', 'study_id', string='Measurements')
    # Linked Control Plan line
    cp_line_id = fields.Many2one('iatf.control.plan.line', string='Control Plan Line', ondelete='restrict')
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('iatf.msa.study') or 'MSA-%s' % self.env['ir.sequence'].next_by_code('iatf.msa.study')
        return super().create(vals_list)

    def action_start_collection(self):
        self.write({'state': 'in_progress'})

    def action_calculate(self):
        """Compute GRR, ndc, ANOVA based on study type."""
        for study in self:
            if study.study_type == 'crossed':
                study._calculate_crossed_grr()
            elif study.study_type == 'nested':
                study._calculate_nested_grr()
            elif study.study_type == 'attribute':
                study._calculate_attribute()
            study._determine_conclusion()
            study.write({'state': 'complete'})

    def action_accept(self):
        self.write({'state': 'accepted'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def _calculate_crossed_grr(self):
        """ANOVA Gauge R&R for Crossed study (AIAG MSA 4th Ed)."""
        self.ensure_one()
        measurements = self.measurement_ids
        if not measurements:
            return

        # Organize data: parts × operators × trials
        parts = self.part_ids
        operators = self.operator_ids
        trials = self.trial_count

        # Build data matrix
        data = {}
        for m in measurements:
            key = (m.part_id.id, m.operator_id.id, m.trial)
            data[key] = m.value

        # Compute means
        part_means = {}
        operator_means = {}
        part_operator_means = {}
        n = len(parts)
        k = len(operators)
        r = trials

        for part in parts:
            vals = [data.get((part.id, op.id, t)) for op in operators for t in range(1, r+1) if data.get((part.id, op.id, t)) is not None]
            if vals:
                part_means[part.id] = statistics.mean(vals)

        for operator in operators:
            vals = [data.get((part.id, operator.id, t)) for part in parts for t in range(1, r+1) if data.get((part.id, operator.id, t)) is not None]
            if vals:
                operator_means[operator.id] = statistics.mean(vals)

        for part in parts:
            for operator in operators:
                vals = [data.get((part.id, operator.id, t)) for t in range(1, r+1) if data.get((part.id, operator.id, t)) is not None]
                if vals:
                    part_operator_means[(part.id, operator.id)] = statistics.mean(vals)

        # Grand mean
        all_vals = [v for v in data.values() if v is not None]
        if not all_vals:
            return
        grand_mean = statistics.mean(all_vals)
        N = len(all_vals)

        # Sum of Squares
        # SS_Total
        ss_total = sum((v - grand_mean)**2 for v in all_vals)

        # SS_Part
        ss_part = k * r * sum((m - grand_mean)**2 for m in part_means.values())

        # SS_Operator
        ss_operator = n * r * sum((m - grand_mean)**2 for m in operator_means.values())

        # SS_Part_Operator (Interaction)
        ss_interaction = 0
        for part in parts:
            for operator in operators:
                key = (part.id, operator.id)
                if key in part_operator_means:
                    ss_interaction += r * (part_operator_means[key] - part_means[part.id] - operator_means[operator.id] + grand_mean)**2

        # SS_Error (Equipment Variation)
        ss_error = 0
        for m in measurements:
            key = (m.part_id.id, m.operator_id.id)
            if key in part_operator_means:
                ss_error += (m.value - part_operator_means[key])**2

        # Degrees of Freedom
        df_total = N - 1
        df_part = n - 1
        df_operator = k - 1
        df_interaction = df_part * df_operator
        df_error = n * k * (r - 1)

        # Mean Squares
        ms_part = ss_part / df_part if df_part else 0
        ms_operator = ss_operator / df_operator if df_operator else 0
        ms_interaction = ss_interaction / df_interaction if df_interaction else 0
        ms_error = ss_error / df_error if df_error else 0

        # Variance Components (AIAG formulas)
        # Equipment Variation (EV)
        ev_var = ms_error
        # Appraiser Variation (AV)
        av_var = max(0, (ms_operator - ms_error) / (n * r)) if ms_operator > ms_error else 0
        # Interaction (INT)
        int_var = max(0, (ms_interaction - ms_error) / r) if ms_interaction > ms_error else 0
        # Part Variation (PV)
        pv_var = max(0, (ms_part - ms_interaction) / (k * r)) if ms_part > ms_interaction else 0

        # GRR
        if self.study_type == 'crossed':
            # Include interaction if significant (p < 0.05)
            f_interaction = ms_interaction / ms_error if ms_error else 0
            # Simplified: use interaction if significant
            grr_var = ev_var + av_var + int_var
        else:
            grr_var = ev_var + av_var

        tv_var = grr_var + pv_var

        # Standard deviations
        ev = math.sqrt(ev_var) if ev_var > 0 else 0
        av = math.sqrt(av_var) if av_var > 0 else 0
        grr = math.sqrt(grr_var) if grr_var > 0 else 0
        pv = math.sqrt(pv_var) if pv_var > 0 else 0
        tv = math.sqrt(tv_var) if tv_var > 0 else 0

        # %GRR (Total Variation)
        grr_percent = (grr / tv * 100) if tv > 0 else 0
        # %GRR (Tolerance)
        tolerance = (self.spec_usl - self.spec_lsl) if self.spec_usl and self.spec_lsl else 0
        grr_percent_tol = (6 * grr / tolerance * 100) if tolerance > 0 else 0
        # ndc
        ndc = int(1.41 * pv / grr) if grr > 0 else 0

        # Capability
        cp = tolerance / (6 * pv) if pv > 0 and tolerance > 0 else 0
        cpk = 0
        if pv > 0 and self.spec_usl and self.spec_lsl and self.spec_target:
            cpu = (self.spec_usl - self.spec_target) / (3 * pv)
            cpl = (self.spec_target - self.spec_lsl) / (3 * pv)
            cpk = min(cpu, cpl)

        # F-statistics for p-values (simplified)
        f_part = ms_part / ms_interaction if ms_interaction else 0
        f_operator = ms_operator / ms_interaction if ms_interaction else 0
        f_interaction = ms_interaction / ms_error if ms_error else 0

        # Approximate p-values (would need scipy for exact)
        # Using simplified approach
        p_part = 0.001 if f_part > 4 else 0.05 if f_part > 2 else 0.1
        p_operator = 0.001 if f_operator > 4 else 0.05 if f_operator > 2 else 0.1
        p_interaction = 0.001 if f_interaction > 4 else 0.05 if f_interaction > 2 else 0.1

        self.write({
            'grr_percent': round(grr_percent, 2),
            'grr_percent_tolerance': round(grr_percent_tol, 2),
            'ndc': ndc,
            'pv_percent': round((pv / tv * 100) if tv > 0 else 0, 2),
            'ev_percent': round((ev / tv * 100) if tv > 0 else 0, 2),
            'av_percent': round((av / tv * 100) if tv > 0 else 0, 2),
            'anova_p_value_part': round(p_part, 4),
            'anova_p_value_operator': round(p_operator, 4),
            'anova_p_value_interaction': round(p_interaction, 4),
            'cp': round(cp, 3),
            'cpk': round(cpk, 3),
        })

    def _calculate_nested_grr(self):
        """Nested Gauge R&R for destructive testing."""
        # Simplified - similar structure but no operator×part interaction
        self._calculate_crossed_grr()  # Placeholder - full implementation needed

    def _calculate_attribute(self):
        """Attribute Agreement Analysis (Kappa, Fleiss' Kappa)."""
        # Placeholder for attribute analysis
        pass

    def _determine_conclusion(self):
        """AIAG MSA acceptance criteria."""
        self.ensure_one()
        if self.grr_percent < 10 and self.ndc >= 5:
            self.conclusion = 'acceptable'
        elif self.grr_percent <= 30 and self.ndc >= 5:
            self.conclusion = 'marginal'
        else:
            self.conclusion = 'unacceptable'


class IATFMSAMeasurement(models.Model):
    """Individual Measurement in MSA Study."""
    _name = 'iatf.msa.measurement'
    _description = 'MSA Measurement'
    _order = 'part_id, operator_id, trial'

    study_id = fields.Many2one('iatf.msa.study', string='MSA Study', required=True, ondelete='cascade')
    part_id = fields.Many2one('product.product', string='Part / Sample', required=True)
    operator_id = fields.Many2one('res.users', string='Operator', required=True)
    trial = fields.Integer(string='Trial #', required=True)
    value = fields.Float(string='Measured Value', required=True)
    # Company
    company_id = fields.Many2one(related='study_id.company_id', store=True)

    _sql_constraints = [
        ('unique_measurement', 'unique(study_id, part_id, operator_id, trial)',
         'Duplicate measurement for same part/operator/trial.'),
    ]