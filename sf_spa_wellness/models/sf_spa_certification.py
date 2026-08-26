from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaCertification(models.Model):
    _name = 'sf.spa.certification'
    _description = 'Spa Therapist Certification'
    _inherit = ['sf.spa.company.mixin', 'mail.thread']
    _order = 'expiry_date'

    name = fields.Char(string='Name', required=True)
    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', required=True, ondelete='cascade')
    cert_type = fields.Char(string='Type', required=True)
    issuing_body = fields.Char(string='Issuing Body')
    issue_date = fields.Date(string='Issue Date')
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    document = fields.Binary(string='Document')
    document_filename = fields.Char(string='Document Filename')
    state = fields.Selection([
        ('valid', 'Valid'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_state', store=True)

    @api.depends('expiry_date')
    def _compute_state(self):
        today = fields.Date.today()
        for record in self:
            if not record.expiry_date:
                record.state = 'valid'
            elif record.expiry_date < today:
                record.state = 'expired'
            elif record.expiry_date <= today + timedelta(days=30):
                record.state = 'expiring'
            else:
                record.state = 'valid'

    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if record.issue_date and record.expiry_date and record.issue_date > record.expiry_date:
                raise ValidationError(_('Issue date must be before expiry date.'))

    from datetime import timedelta