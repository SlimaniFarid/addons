from odoo import api, fields, models


class QMSFMEA(models.Model):
    _name = 'qms.fmea'
    _description = 'FMEA (Failure Mode and Effects Analysis)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='FMEA Name', required=True)
    fmea_type = fields.Selection([
        ('dfmea', 'Design FMEA (DFMEA)'),
        ('pfmea', 'Process FMEA (PFMEA)'),
    ], string='Type', required=True)

    product_id = fields.Many2one('product.product', string='Product/Process')
    process_id = fields.Many2one('qms.process', string='Process')

    # Team
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')

    # Scope
    scope = fields.Html(string='Scope')
    boundary = fields.Html(string='Boundary Diagram')

    # Items
    item_ids = fields.One2many('qms.fmea.item', 'fmea_id', string='Items')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)

    approved_by_id = fields.Many2one('res.users', string='Approved By')
    approved_date = fields.Date(string='Approved Date')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qms.fmea') or 'FMEA-%s' % self.env['ir.sequence'].next_by_code('qms.fmea')
        return super().create(vals_list)


class QMSFMEAItem(models.Model):
    _name = 'qms.fmea.item'
    _description = 'FMEA Item'
    _order = 'sequence, id'

    fmea_id = fields.Many2one('qms.fmea', string='FMEA', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    # Function/Step
    function = fields.Char(string='Function / Process Step', required=True)
    requirement = fields.Char(string='Requirement')

    # Failure
    failure_mode = fields.Char(string='Failure Mode', required=True)
    failure_cause = fields.Char(string='Failure Cause', required=True)
    failure_effect = fields.Char(string='Failure Effect', required=True)

    # Current Controls
    prevention_control = fields.Char(string='Prevention Control')
    detection_control = fields.Char(string='Detection Control')

    # Ratings (1-10)
    severity = fields.Integer(string='Severity (S)', required=True, default=1)
    occurrence = fields.Integer(string='Occurrence (O)', required=True, default=1)
    detection = fields.Integer(string='Detection (D)', required=True, default=1)

    # RPN
    rpn = fields.Integer(string='RPN (S x O x D)', compute='_compute_rpn', store=True)
    rpn_class = fields.Selection([
        ('low', 'Low (1-50)'),
        ('medium', 'Medium (51-150)'),
        ('high', 'High (151-350)'),
        ('critical', 'Critical (351-1000)'),
    ], string='RPN Class', compute='_compute_rpn', store=True)

    # Recommended Actions
    recommended_action = fields.Text(string='Recommended Action')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    target_date = fields.Date(string='Target Date')

    # After Action
    action_taken = fields.Text(string='Action Taken')
    new_severity = fields.Integer(string='New S')
    new_occurrence = fields.Integer(string='New O')
    new_detection = fields.Integer(string='New D')
    new_rpn = fields.Integer(string='New RPN', compute='_compute_new_rpn', store=True)

    @api.depends('severity', 'occurrence', 'detection')
    def _compute_rpn(self):
        for item in self:
            item.rpn = item.severity * item.occurrence * item.detection
            if item.rpn <= 50:
                item.rpn_class = 'low'
            elif item.rpn <= 150:
                item.rpn_class = 'medium'
            elif item.rpn <= 350:
                item.rpn_class = 'high'
            else:
                item.rpn_class = 'critical'

    @api.depends('new_severity', 'new_occurrence', 'new_detection')
    def _compute_new_rpn(self):
        for item in self:
            if item.new_severity and item.new_occurrence and item.new_detection:
                item.new_rpn = item.new_severity * item.new_occurrence * item.new_detection
            else:
                item.new_rpn = 0