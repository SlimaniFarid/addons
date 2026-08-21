# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfAqlInspection(models.Model):
    _name = 'sf.aql.inspection'
    _description = 'AQL Lot Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'inspection_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    plan_id = fields.Many2one('sf.aql.plan', string='Sampling Plan', ondelete='set null')
    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 ondelete='restrict')
    lot_id = fields.Many2one('stock.lot', string='Lot', ondelete='set null')
    partner_id = fields.Many2one('res.partner', string='Supplier', ondelete='set null')
    source = fields.Selection([
        ('incoming', 'Incoming'),
        ('production', 'Production'),
        ('final', 'Final'),
    ], string='Source', required=True, default='incoming')
    inspection_level = fields.Selection([
        ('I', 'Level I'),
        ('II', 'Level II'),
        ('III', 'Level III'),
    ], string='Inspection Level', required=True, default='II')
    lot_quantity = fields.Float(string='Lot Quantity', required=True, default=1.0)
    sample_size = fields.Integer(string='Sample Size', compute='_compute_sample_size',
                                 store=True)
    defect_ids = fields.One2many('sf.aql.defect', 'inspection_id', string='Defects')
    critical_defects = fields.Integer(string='Critical Defects',
                                      compute='_compute_defect_stats', store=True)
    weighted_defects = fields.Integer(string='Weighted Defects',
                                      compute='_compute_defect_stats', store=True)
    decision = fields.Selection([
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Decision', compute='_compute_decision', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('released', 'Released'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    inspection_date = fields.Date(string='Inspection Date', required=True,
                                  default=fields.Date.context_today)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_lot_quantity_positive',
         'CHECK (lot_quantity > 0)',
         'The lot quantity must be greater than zero.'),
    ]

    @api.constrains('lot_quantity')
    def _check_lot_quantity(self):
        for inspection in self:
            if inspection.lot_quantity <= 0:
                raise ValidationError(_('The lot quantity must be greater than zero.'))

    @api.depends('plan_id.sample_size', 'lot_quantity')
    def _compute_sample_size(self):
        for inspection in self:
            if inspection.plan_id:
                inspection.sample_size = inspection.plan_id.sample_size
            else:
                inspection.sample_size = int(round(inspection.lot_quantity))

    @api.depends('defect_ids.severity', 'defect_ids.quantity')
    def _compute_defect_stats(self):
        weights = {'critical': 10, 'major': 5, 'minor': 1}
        for inspection in self:
            critical = 0
            total = 0
            for defect in inspection.defect_ids:
                total += defect.quantity * weights[defect.severity]
                if defect.severity == 'critical':
                    critical += defect.quantity
            inspection.critical_defects = critical
            inspection.weighted_defects = total

    @api.depends('critical_defects', 'weighted_defects', 'plan_id.reject_number',
                 'defect_ids.quantity', 'defect_ids.severity')
    def _compute_decision(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_aql_sampling.enable_weighted_defects')
        weighted = param == 'True' if param else True
        for inspection in self:
            if not inspection.plan_id:
                inspection.decision = 'accepted'
                continue
            if inspection.critical_defects:
                inspection.decision = 'rejected'
                continue
            if weighted:
                exceeded = inspection.weighted_defects > inspection.plan_id.reject_number
            else:
                raw = sum(d.quantity for d in inspection.defect_ids)
                exceeded = raw > inspection.plan_id.reject_number
            inspection.decision = 'rejected' if exceeded else 'accepted'

    def _default_inspection_level(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_aql_sampling.default_inspection_level')
        return param if param in ('I', 'II', 'III') else 'II'

    @api.model
    def _find_plan(self, lot_quantity, inspection_level):
        lot_qty = int(round(lot_quantity))
        plans = self.env['sf.aql.plan'].search([
            ('inspection_level', '=', inspection_level),
            ('lot_size_min', '<=', lot_qty),
            ('lot_size_max', '>=', lot_qty),
        ], order='lot_size_min asc, sample_size asc', limit=1)
        return plans.id or False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.aql.inspection')
            if not vals.get('inspection_level'):
                vals['inspection_level'] = self._default_inspection_level()
            if not vals.get('plan_id') and vals.get('lot_quantity'):
                vals['plan_id'] = self._find_plan(
                    vals['lot_quantity'], vals.get('inspection_level', 'II'))
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_aql_sampling.group_sf_aql_sampling_manager'):
            raise UserError(_('Only an AQL sampling manager can perform this action.'))

    def action_start(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft inspections can be started.'))
        self.state = 'in_progress'

    def action_complete(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress inspections can be completed.'))
        self.state = 'completed'

    def action_release(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'completed':
            raise UserError(_('Only completed inspections can be released.'))
        if self.decision != 'accepted':
            raise UserError(_('A rejected inspection cannot be released.'))
        self.state = 'released'

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'completed':
            raise UserError(_('Only completed inspections can be rejected.'))
        if self.decision != 'rejected':
            raise UserError(_('An accepted inspection cannot be rejected without a critical defect. A manager can force rejection by setting the decision to rejected first.'))
        self.state = 'rejected'

    def action_force_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'completed':
            raise UserError(_('Only completed inspections can be rejected.'))
        self.decision = 'rejected'
        self.state = 'rejected'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('released', 'rejected', 'cancelled'):
            raise UserError(_('A released, rejected or cancelled inspection cannot be cancelled.'))
        self.state = 'cancelled'