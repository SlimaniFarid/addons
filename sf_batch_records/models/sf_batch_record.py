# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfBatchRecord(models.Model):
    _name = 'sf.batch.record'
    _description = 'Batch Production Record'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.batch.record.activity.mixin']
    _order = 'production_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 ondelete='restrict')
    product_lot_id = fields.Many2one('stock.lot', string='Output Lot', ondelete='set null')
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    uom_name = fields.Char(string='Unit of Measure')
    production_date = fields.Date(string='Production Date', required=True,
                                  default=fields.Date.context_today)
    mo_reference = fields.Char(string='Manufacturing Order Ref.')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('under_review', 'Under Review'),
        ('released', 'Released'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    material_ids = fields.One2many('sf.batch.record.material', 'batch_record_id',
                                   string='Materials')
    step_ids = fields.One2many('sf.batch.record.step', 'batch_record_id', string='Steps')
    parameter_ids = fields.One2many('sf.batch.record.parameter', 'batch_record_id',
                                    string='Parameters')
    deviation_ids = fields.One2many('sf.batch.record.deviation', 'batch_record_id',
                                    string='Deviations')
    out_of_spec_params = fields.Integer(string='Out-of-Spec Parameters',
                                        compute='_compute_out_of_spec_params', store=True)
    reviewed_by = fields.Many2one('res.users', string='Reviewed By', readonly=True)
    reviewed_on = fields.Datetime(string='Reviewed On', readonly=True)
    released_by = fields.Many2one('res.users', string='Released By', readonly=True)
    released_on = fields.Datetime(string='Released On', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_quantity_positive',
         'CHECK (quantity > 0)',
         'The batch quantity must be greater than zero.'),
    ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_('The batch quantity must be greater than zero.'))

    @api.depends('parameter_ids.status', 'deviation_ids.state', 'deviation_ids.parameter_id')
    def _compute_out_of_spec_params(self):
        for record in self:
            count = 0
            for param in record.parameter_ids:
                if param.status == 'out_of_spec':
                    covered = record.deviation_ids.filtered(
                        lambda d: d.state == 'approved' and d.parameter_id == param)
                    if not covered:
                        count += 1
            record.out_of_spec_params = count

    def _check_manager(self):
        if not self.env.user.has_group('sf_batch_records.group_sf_batch_records_manager'):
            raise UserError(_('Only a batch records manager can perform this action.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.batch.record')
        return super().create(vals_list)

    def action_start(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft batch records can be started.'))
        self.state = 'in_progress'

    def action_submit_review(self):
        self.ensure_one()
        if self.state not in ('draft', 'in_progress'):
            raise UserError(_('Only draft or in-progress batch records can be submitted for review.'))
        self.write({
            'state': 'under_review',
            'reviewed_by': self.env.user.id,
            'reviewed_on': fields.Datetime.now(),
        })

    def action_release(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'under_review':
            raise UserError(_('Only batch records under review can be released.'))
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_batch_records.block_out_of_spec_release')
        block = param == 'True' if param else True
        if block and self.out_of_spec_params:
            raise UserError(_(
                'Release blocked: %s parameter(s) are out of specification without an '
                'approved deviation.') % self.out_of_spec_params)
        self.write({
            'state': 'released',
            'released_by': self.env.user.id,
            'released_on': fields.Datetime.now(),
        })

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'under_review':
            raise UserError(_('Only batch records under review can be rejected.'))
        self.state = 'rejected'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('released', 'rejected', 'cancelled'):
            raise UserError(_('A released, rejected or cancelled batch record cannot be cancelled.'))
        self.state = 'cancelled'