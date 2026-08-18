from odoo import api, fields, models


class QMSCapa(models.Model):
    _name = 'qms.capa'
    _description = 'Corrective and Preventive Action (CAPA)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='CAPA Number', required=True, copy=False, default='New')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    nc_id = fields.Many2one('qms.nc', string='Source NC', ondelete='set null')
    title = fields.Char(string='CAPA Title', required=True)
    description = fields.Html(string='Description')

    capa_type = fields.Selection([
        ('corrective', 'Corrective Action'),
        ('preventive', 'Preventive Action'),
        ('both', 'Corrective & Preventive'),
    ], string='Type', required=True, default='corrective')

    # Root cause link
    root_cause = fields.Html(string='Root Cause Summary')

    # Actions
    action_ids = fields.One2many('qms.capa.action', 'capa_id', string='Actions')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('implementation', 'Implementation'),
        ('verification', 'Effectiveness Verification'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Ownership
    owner_id = fields.Many2one('res.users', string='CAPA Owner', default=lambda s: s.env.user, required=True)
    team_ids = fields.Many2many('res.users', string='Team Members')

    # Dates
    target_date = fields.Date(string='Target Completion Date')
    completion_date = fields.Date(string='Actual Completion Date')

    # Verification
    effectiveness_method = fields.Selection([
        ('audit', 'Follow-up Audit'),
        ('inspection', 'Inspection'),
        ('data_analysis', 'Data Analysis / KPIs'),
        ('customer_feedback', 'Customer Feedback'),
        ('other', 'Other'),
    ], string='Verification Method')
    effectiveness_criteria = fields.Html(string='Effectiveness Criteria')
    effectiveness_result = fields.Selection([
        ('effective', 'Effective'),
        ('partially_effective', 'Partially Effective'),
        ('not_effective', 'Not Effective'),
    ], string='Verification Result')
    verification_date = fields.Date(string='Verification Date')
    verified_by_id = fields.Many2one('res.users', string='Verified By')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qms.capa') or 'CAPA-%s' % self.env['ir.sequence'].next_by_code('qms.capa')
        return super().create(vals_list)

    def action_plan(self):
        self.write({'state': 'planned'})

    def action_implement(self):
        self.write({'state': 'implementation'})

    def action_verify(self):
        self.write({'state': 'verification'})

    def action_close(self):
        self.write({'state': 'closed', 'completion_date': fields.Date.today()})


class QMSCapaAction(models.Model):
    _name = 'qms.capa.action'
    _description = 'CAPA Action Item'

    capa_id = fields.Many2one('qms.capa', string='CAPA', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    description = fields.Html(string='Action Description', required=True)
    action_type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive'),
        ('improvement', 'Improvement'),
    ], string='Type', required=True)

    responsible_id = fields.Many2one('res.users', string='Responsible', required=True)
    due_date = fields.Date(string='Due Date')
    completion_date = fields.Date(string='Completion Date')

    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', tracking=True)

    evidence = fields.Html(string='Evidence of Completion')
    evidence_attachment_ids = fields.Many2many('ir.attachment', string='Evidence Attachments')

    def action_complete(self):
        self.write({'state': 'done', 'completion_date': fields.Date.today()})
        # Check if all actions done -> move CAPA to verification
        if all(a.state == 'done' for a in self.capa_id.action_ids):
            self.capa_id.write({'state': 'verification'})