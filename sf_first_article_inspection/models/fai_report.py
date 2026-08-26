# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FAIReport(models.Model):
    _name = 'sf.fai.report'
    _description = 'First Article Inspection Report'
    _rec_name = 'display_name'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    display_name = fields.Char(string='FAI Number', compute='_compute_display_name', store=True)
    part_id = fields.Many2one('product.product', string='Part', required=True)
    part_revision = fields.Char(string='Part Revision')
    drawing_number = fields.Char(string='Drawing Number')
    drawing_revision = fields.Char(string='Drawing Revision')
    supplier_id = fields.Many2one('res.partner', string='Supplier', domain=[('supplier_rank', '>', 0)])
    customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer_rank', '>', 0)])
    po_number = fields.Char(string='PO Number')
    fai_type = fields.Selection([
        ('full', 'Full FAI'),
        ('partial', 'Partial FAI'),
        ('delta', 'Delta FAI'),
    ], string='FAI Type', default='full', required=True)
    reason_partial = fields.Text(string='Reason for Partial/Delta')
    date = fields.Date(string='FAI Date', default=fields.Date.today, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    characteristic_ids = fields.One2many('sf.fai.characteristic', 'report_id', string='Characteristics')
    nonconformance_ids = fields.One2many('sf.fai.nonconformance', 'report_id', string='Non-conformances')
    approval_ids = fields.One2many('sf.fai.approval', 'report_id', string='Approvals')
    total_characteristics = fields.Integer(string='Total Characteristics', compute='_compute_counts', store=True)
    passed_characteristics = fields.Integer(string='Passed', compute='_compute_counts', store=True)
    failed_characteristics = fields.Integer(string='Failed', compute='_compute_counts', store=True)
    accountability_pct = fields.Float(string='Accountability %', compute='_compute_counts', store=True)
    balloon_drawing = fields.Binary(string='Ballooned Drawing', attachment=True)
    balloon_filename = fields.Char(string='Balloon Filename')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('part_fai_type_uniq', 'unique(part_id, fai_type, date)',
         'Only one FAI per part/type/date combination.'),
    ]

    @api.depends('part_id', 'date', 'id')
    def _compute_display_name(self):
        for report in self:
            report.display_name = f"FAI-{report.id:06d}"

    @api.depends('characteristic_ids', 'characteristic_ids.result')
    def _compute_counts(self):
        for report in self:
            chars = report.characteristic_ids
            report.total_characteristics = len(chars)
            report.passed_characteristics = len(chars.filtered(lambda c: c.result == 'pass'))
            report.failed_characteristics = len(chars.filtered(lambda c: c.result == 'fail'))
            report.accountability_pct = report.total_characteristics and (
                report.passed_characteristics / report.total_characteristics * 100) or 0.0

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_submit(self):
        self.write({'state': 'submitted'})
        # Create approval records for required approvers
        for report in self:
            if not report.approval_ids:
                # Add default approvals - supplier quality, customer quality
                self.env['sf.fai.approval'].create([
                    {'report_id': report.id, 'role': 'supplier_quality', 'user_id': report.create_uid.id},
                    {'report_id': report.id, 'role': 'customer_quality'},
                ])

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_close(self):
        self.write({'state': 'closed'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.fai.approval'

    def action_refresh_business(self):
        """Pull active MO count and average yield."""
        Mos = self.env['mrp.production']
        active = Mos.search([('state', 'in', ('confirmed', 'progress'))])
        done = Mos.search([('state', '=', 'done')], limit=50)
        yields = [(mo.qty_produced / mo.product_qty * 100)
                  for mo in done if mo.product_qty]
        avg_yield = sum(yields) / len(yields) if yields else 0.0
        for rec in self:
            rec.message_post(body=_(
                '{a} active MO(s), avg yield {y:.1f}% on last {d} done.')
                .format(a=len(active), y=avg_yield, d=len(done)))
        return True
