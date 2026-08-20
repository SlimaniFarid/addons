from odoo import api, fields, models


class QMSReviewInput(models.Model):
    _name = 'qms.review.input'
    _description = 'Management Review Input'

    review_id = fields.Many2one('qms.review', string='Review', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    category = fields.Selection([
        ('audit_results', 'Audit Results'),
        ('customer_feedback', 'Customer Feedback'),
        ('process_performance', 'Process Performance / Product Conformity'),
        ('nc_capa_status', 'NC / CAPA Status'),
        ('previous_actions', 'Follow-up from Previous Reviews'),
        ('changes', 'Changes Affecting QMS'),
        ('resource_needs', 'Resource Needs'),
        ('risk_opportunity', 'Risk & Opportunity'),
        ('supplier_performance', 'Supplier Performance'),
        ('training', 'Training Effectiveness'),
    ], string='Category', required=True)

    description = fields.Html(string='Details / Summary')
    metrics = fields.Html(string='Key Metrics / KPIs')
    presenter_id = fields.Many2one('res.users', string='Presenter')
    attachments = fields.Many2many('ir.attachment', string='Supporting Documents')