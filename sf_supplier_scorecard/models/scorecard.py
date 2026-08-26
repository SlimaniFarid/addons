# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SupplierScorecard(models.Model):
    _name = 'sf.supplier.scorecard'
    _description = 'Supplier Scorecard'
    _rec_name = 'partner_id'
    _order = 'period desc'

    partner_id = fields.Many2one('res.partner', string='Supplier',
                                 required=True)
    period = fields.Selection([
        ('month', 'Monthly'),
        ('quarter', 'Quarterly'),
        ('year', 'Yearly'),
    ], string='Period', default='month', required=True)
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    on_time_pct = fields.Float(string='On-Time Delivery %', default=0.0)
    defect_rate = fields.Float(string='Defect Rate %', default=0.0)
    quality_score = fields.Float(string='Quality Score', default=0.0)
    compliance_score = fields.Float(string='Compliance Score', default=0.0)
    on_time_weight = fields.Float(string='Delivery Weight', default=30.0)
    defect_weight = fields.Float(string='Defect Weight', default=30.0)
    quality_weight = fields.Float(string='Quality Weight', default=25.0)
    compliance_weight = fields.Float(string='Compliance Weight', default=15.0)
    overall_score = fields.Float(string='Overall Score', compute='_compute_overall',
                                 store=True)
    rating = fields.Selection([
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ], string='Rating', compute='_compute_overall', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.depends('on_time_pct', 'defect_rate', 'quality_score',
                 'compliance_score', 'on_time_weight', 'defect_weight',
                 'quality_weight', 'compliance_weight')
    def _compute_overall(self):
        for sc in self:
            total_weight = (sc.on_time_weight + sc.defect_weight +
                            sc.quality_weight + sc.compliance_weight)
            if not total_weight:
                sc.overall_score = 0.0
                sc.rating = 'poor'
                continue
            quality = max(0.0, 100.0 - sc.defect_rate)
            score = ((sc.on_time_pct * sc.on_time_weight +
                      quality * sc.defect_weight +
                      sc.quality_score * sc.quality_weight +
                      sc.compliance_score * sc.compliance_weight)
                     / total_weight)
            sc.overall_score = round(score, 1)
            if sc.overall_score >= 90:
                sc.rating = 'excellent'
            elif sc.overall_score >= 75:
                sc.rating = 'good'
            elif sc.overall_score >= 60:
                sc.rating = 'fair'
            else:
                sc.rating = 'poor'

    def action_publish(self):
        for sc in self:
            sc.state = 'published'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier.issue'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2Scorecard(models.Model):
    _inherit = 'sf.supplier.scorecard'

    def action_compute(self):
        """OTIF from receipts, defect rate from logged supplier issues,
        quality proxy from resolved ratio; weighted overall score."""
        self.ensure_one()
        start = self.date_from
        end = self.date_to or fields.Date.context_today(self)

        # --- On-time delivery: receipts of this partner's POs in window
        picks = self.env['stock.picking'].search([
            ('partner_id', '=', self.partner_id.id),
            ('picking_type_code', '=', 'incoming'),
            ('state', '=', 'done'),
            ('date_done', '>=', start),
            ('date_done', '<=', end),
        ])
        total_picks = len(picks)
        on_time = len([p for p in picks
                       if p.date_deadline
                       and p.date_of_done.date() <= p.date_deadline])
        on_time_pct = (on_time / total_picks * 100.0) if total_picks else 0.0

        # --- Defects from issue log (module-native model)
        Issue = self.env['sf.supplier.issue']
        issues = Issue.search([
            ('partner_id', '=', self.partner_id.id),
            ('date', '>=', start), ('date', '<=', end)])
        defect_rate = float(len(issues))  # issues count as raw defect signal

        resolved = issues.filtered('resolved')
        quality_score = (len(resolved) / len(issues) * 100.0)             if issues else 100.0
        compliance_score = 100.0 - min(len(issues) * 5.0, 40.0)

        overall = (on_time_pct * (self.on_time_weight or 0)
                   + (100.0 - min(defect_rate * 10, 100))
                   * (self.defect_weight or 0)
                   + quality_score * (self.quality_weight or 0)
                   + compliance_score * (self.compliance_weight or 0))
        rating = 'A' if overall >= 85 else 'B' if overall >= 70 \
            else 'C' if overall >= 55 else 'D'
        self.write({
            'on_time_pct': round(on_time_pct, 1),
            'defect_rate': defect_rate,
            'quality_score': round(quality_score, 1),
            'compliance_score': round(compliance_score, 1),
            'overall_score': round(overall, 1),
            'rating': rating,
        })
        self.message_post(body=_(
            'Scorecard computed: OTIF %.1f%% on %s receipt(s); '
            '%s issue(s); overall %.1f -> %s.')
            % (on_time_pct, total_picks, len(issues), overall, rating))
        return True
