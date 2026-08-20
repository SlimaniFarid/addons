from odoo import api, fields, models


class QMSReviewOutput(models.Model):
    _name = 'qms.review.output'
    _description = 'Management Review Output'

    review_id = fields.Many2one('qms.review', string='Review', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    category = fields.Selection([
        ('improvement', 'Improvement Opportunities'),
        ('changes_qms', 'Changes to QMS'),
        ('resource_needs', 'Resource Needs'),
        ('training', 'Training Needs'),
        ('policy_objectives', 'Policy / Objectives Update'),
        ('other', 'Other'),
    ], string='Category', required=True)

    action = fields.Html(string='Action Required', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    target_date = fields.Date(string='Target Date')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open')
    evidence = fields.Html(string='Evidence of Completion')