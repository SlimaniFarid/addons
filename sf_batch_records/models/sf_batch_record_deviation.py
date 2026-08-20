# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfBatchRecordDeviation(models.Model):
    _name = 'sf.batch.record.deviation'
    _description = 'Batch Record Deviation'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.batch.record.activity.mixin']
    _order = 'id desc'

    batch_record_id = fields.Many2one('sf.batch.record', string='Batch Record',
                                      required=True, ondelete='cascade', index=True)
    display_name = fields.Char(string='Reference', compute='_compute_display_name')
    description = fields.Text(string='Description', required=True)
    category = fields.Selection([
        ('material', 'Material'),
        ('parameter', 'Parameter'),
        ('process', 'Process'),
        ('other', 'Other'),
    ], string='Category', default='parameter')
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', default='minor')
    parameter_id = fields.Many2one('sf.batch.record.parameter', string='Linked Parameter',
                                   ondelete='set null')
    corrective_action = fields.Text(string='Corrective Action')
    state = fields.Selection([
        ('open', 'Open'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='open', copy=False)
    resolved_by = fields.Many2one('res.users', string='Resolved By', readonly=True)
    resolved_on = fields.Datetime(string='Resolved On', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.depends('id')
    def _compute_display_name(self):
        for deviation in self:
            deviation.display_name = 'DEV-%05d' % deviation.id

    def _check_manager(self):
        if not self.env.user.has_group('sf_batch_records.group_sf_batch_records_manager'):
            raise UserError(_('Only a batch records manager can approve or reject deviations.'))

    def action_approve(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'open':
            raise UserError(_('Only open deviations can be approved.'))
        self.write({
            'state': 'approved',
            'resolved_by': self.env.user.id,
            'resolved_on': fields.Datetime.now(),
        })

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'open':
            raise UserError(_('Only open deviations can be rejected.'))
        self.write({
            'state': 'rejected',
            'resolved_by': self.env.user.id,
            'resolved_on': fields.Datetime.now(),
        })