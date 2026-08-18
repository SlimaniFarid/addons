from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QMSTraining(models.Model):
    _name = 'qms.training'
    _description = 'Training & Competence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Training Name', required=True)
    code = fields.Char(string='Training Code', required=True, copy=False)

    # Scope
    category = fields.Selection([
        ('induction', 'Induction'),
        ('job_specific', 'Job Specific'),
        ('safety', 'Health & Safety'),
        ('quality', 'Quality System'),
        ('regulatory', 'Regulatory'),
        ('skills', 'Technical Skills'),
        ('management', 'Management'),
        ('other', 'Other'),
    ], string='Category', required=True)

    # Content
    description = fields.Html(string='Description')
    objectives = fields.Html(string='Learning Objectives')
    duration_hours = fields.Float(string='Duration (Hours)')

    # Delivery
    delivery_method = fields.Selection([
        ('classroom', 'Classroom'),
        ('online', 'E-Learning'),
        ('on_job', 'On-the-Job'),
        ('external', 'External Provider'),
        ('blended', 'Blended'),
    ], string='Delivery Method', default='classroom')

    trainer_id = fields.Many2one('res.users', string='Trainer')
    external_provider = fields.Char(string='External Provider')

    # Competence
    competence_ids = fields.Many2many('qms.competence', string='Competences Developed')
    prerequisite_ids = fields.Many2many('qms.training', 'training_prereq_rel', 'training_id', 'prereq_id', string='Prerequisites')

    # Evaluation
    has_exam = fields.Boolean(string='Has Exam', default=False)
    passing_score = fields.Float(string='Passing Score (%)', default=70.0)

    # Records
    record_ids = fields.One2many('qms.training.record', 'training_id', string='Training Records')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('qms.training') or 'TRN-%s' % self.env['ir.sequence'].next_by_code('qms.training')
        return super().create(vals_list)


class QMSTrainingRecord(models.Model):
    _name = 'qms.training.record'
    _description = 'Training Record'
    _order = 'training_date desc'

    training_id = fields.Many2one('qms.training', string='Training', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    user_id = fields.Many2one(related='employee_id.user_id', string='User', store=True)

    training_date = fields.Date(string='Training Date', default=fields.Date.today)
    expiry_date = fields.Date(string='Expiry Date')
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
        ('waived', 'Waived'),
    ], string='Status', default='scheduled', tracking=True)

    score = fields.Float(string='Score (%)')
    passed = fields.Boolean(string='Passed')
    certificate_number = fields.Char(string='Certificate Number')
    certificate_attachment = fields.Many2one('ir.attachment', string='Certificate')

    trainer_id = fields.Many2one('res.users', string='Trainer')
    notes = fields.Text(string='Notes')

    @api.onchange('score', 'training_id')
    def _onchange_score(self):
        if self.training_id and self.training_id.has_exam and self.score:
            self.passed = self.score >= self.training_id.passing_score


class QMSCompetence(models.Model):
    _name = 'qms.competence'
    _description = 'Competence Definition'

    name = fields.Char(string='Competence Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Html(string='Description')

    # Requirements
    required_education = fields.Selection([
        ('none', 'None'),
        ('high_school', 'High School'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('certification', 'Professional Certification'),
    ], string='Min Education')

    required_experience_years = fields.Integer(string='Min Experience (Years)')
    required_certifications = fields.Many2many('qms.certification', string='Required Certifications')

    # Training links
    training_ids = fields.Many2many('qms.training', string='Training Programs')

    # Evaluation criteria
    evaluation_criteria = fields.Html(string='Evaluation Criteria')


class QMSCertification(models.Model):
    _name = 'qms.certification'
    _description = 'Professional Certification'

    name = fields.Char(string='Certification Name', required=True)
    code = fields.Char(string='Code', required=True)
    issuing_body = fields.Char(string='Issuing Body')
    validity_years = fields.Integer(string='Validity (Years)')
    renewal_requirements = fields.Text(string='Renewal Requirements')