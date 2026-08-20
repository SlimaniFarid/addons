# -*- coding: utf-8 -*-
from odoo import fields, models, _


class FAIApproval(models.Model):
    _name = 'sf.fai.approval'
    _description = 'FAI Approval'
    _order = 'sequence, id'

    report_id = fields.Many2one('sf.fai.report', string='FAI Report', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    role = fields.Selection([
        ('supplier_quality', 'Supplier Quality Engineer'),
        ('customer_quality', 'Customer Quality Engineer'),
        ('production', 'Production Manager'),
        ('engineering', 'Engineering'),
        ('other', 'Other'),
    ], string='Role', required=True)
    user_id = fields.Many2one('res.users', string='Approver')
    group_id = fields.Many2one('res.groups', string='Approver Group')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delegated', 'Delegated'),
    ], string='Status', default='pending')
    date = fields.Datetime(string='Decision Date')
    comments = fields.Text(string='Comments')

    def action_approve(self):
        self.write({'status': 'approved', 'date': fields.Datetime.now()})
        # Check if all approvals are done
        pending = self.search([('report_id', '=', self.report_id.id), ('status', '=', 'pending')])
        if not pending:
            self.report_id.write({'state': 'approved'})

    def action_reject(self):
        self.write({'status': 'rejected', 'date': fields.Datetime.now()})
        self.report_id.write({'state': 'rejected'})