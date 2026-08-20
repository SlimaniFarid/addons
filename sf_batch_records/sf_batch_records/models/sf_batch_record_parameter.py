# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfBatchRecordParameter(models.Model):
    _name = 'sf.batch.record.parameter'
    _description = 'Batch Record Parameter'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.batch.record.activity.mixin']
    _order = 'id asc'

    batch_record_id = fields.Many2one('sf.batch.record', string='Batch Record',
                                      required=True, ondelete='cascade', index=True)
    step_id = fields.Many2one('sf.batch.record.step', string='Step', ondelete='set null')
    name = fields.Char(string='Parameter', required=True)
    unit = fields.Char(string='Unit')
    expected_value = fields.Float(string='Expected Value')
    min_value = fields.Float(string='Min Value')
    max_value = fields.Float(string='Max Value')
    actual_value = fields.Float(string='Actual Value')
    status = fields.Selection([
        ('in_spec', 'In Specification'),
        ('out_of_spec', 'Out of Specification'),
    ], string='Status', compute='_compute_status', store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.depends('actual_value', 'min_value', 'max_value')
    def _compute_status(self):
        for param in self:
            if (param.actual_value is not None
                    and param.min_value is not None
                    and param.max_value is not None
                    and not (param.min_value <= param.actual_value <= param.max_value)):
                param.status = 'out_of_spec'
            else:
                param.status = 'in_spec'

    def _check_editable(self):
        self.ensure_one()
        if self.batch_record_id.state in ('under_review', 'released', 'rejected', 'cancelled'):
            raise UserError(_('Parameters can only be edited while the batch record is in progress.'))

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('batch_record_id'):
                parent = self.env['sf.batch.record'].browse(vals['batch_record_id'])
                if parent.state in ('under_review', 'released', 'rejected', 'cancelled'):
                    raise UserError(_('Parameters can only be edited while the batch record is in progress.'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._check_editable()
        return super().write(vals)

    def unlink(self):
        for record in self:
            record._check_editable()
        return super().unlink()