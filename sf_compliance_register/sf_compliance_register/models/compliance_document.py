# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ComplianceDocumentType(models.Model):
    _name = 'sf.compliance.document.type'
    _description = 'Compliance Document Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    category = fields.Selection([
        ('license', 'License'),
        ('permit', 'Permit'),
        ('insurance', 'Insurance'),
        ('certification', 'Certification'),
        ('agrement', 'Agreement'),
        ('legal', 'Legal'),
        ('other', 'Other'),
    ], string='Category', default='license')
    default_alert_days = fields.Integer(string='Default Alert Days',
                                        default=30)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name, company_id)',
         'A document type name must be unique per company.'),
    ]


class ComplianceDocument(models.Model):
    _name = 'sf.compliance.document'
    _description = 'Compliance Document'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'expiry_date'

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference', required=True,
                      default=lambda self: _('New'))
    document_type_id = fields.Many2one('sf.compliance.document.type',
                                       string='Type', required=True)
    issuer = fields.Char(string='Issuer')
    partner_id = fields.Many2one('res.partner', string='Issuer Partner')
    issue_date = fields.Date(string='Issue Date', required=True)
    expiry_date = fields.Date(string='Expiry Date', required=True)
    alert_days = fields.Integer(string='Alert Days',
                                compute='_compute_alert_days',
                                store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_state', store=True,
       default='draft')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Attachments')
    published = fields.Boolean(string='Published', default=False)
    renewal_of_id = fields.Many2one('sf.compliance.document',
                                    string='Renewal Of')
    renewed_by_id = fields.Many2one('sf.compliance.document',
                                    string='Renewed By')
    history_ids = fields.One2many('sf.compliance.history',
                                  'document_id',
                                  string='History')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('document_type_id.default_alert_days',
                 'company_id.sf_compliance_default_alert_days')
    def _compute_alert_days(self):
        for doc in self:
            if doc.document_type_id:
                doc.alert_days = doc.document_type_id.default_alert_days
            else:
                doc.alert_days = \
                    doc.company_id.sf_compliance_default_alert_days

    @api.depends('published', 'expiry_date', 'alert_days')
    def _compute_state(self):
        today = fields.Date.today()
        for doc in self:
            if not doc.published:
                doc.state = 'draft'
            elif doc.expiry_date < today:
                doc.state = 'expired'
            elif (doc.expiry_date - today).days <= doc.alert_days:
                doc.state = 'expiring'
            else:
                doc.state = 'active'

    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for doc in self:
            if doc.issue_date and doc.expiry_date:
                if doc.expiry_date <= doc.issue_date:
                    raise UserError(
                        _('The expiry date must be after the issue '
                          'date.'))

    @api.constrains('alert_days')
    def _check_alert_days(self):
        for doc in self:
            if doc.alert_days < 0:
                raise UserError(
                    _('Alert days cannot be negative.'))

    def action_publish(self):
        for doc in self:
            if doc.state != 'draft':
                raise UserError(_('Only draft documents can be '
                                  'published.'))
            if doc.company_id.sf_compliance_require_attachment and \
                    not doc.attachment_ids:
                raise UserError(
                    _('An attachment is required before publishing '
                      'this document.'))
            doc.published = True
            self._write_history(doc, 'created')
            doc.message_post(body=_('Document published.'))

    def action_renew(self):
        self.ensure_one()
        return {
            'name': _('Renew Document'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.compliance.renew.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_document_id': self.id},
        }

    def action_expire(self):
        for doc in self:
            if doc.state != 'expired':
                raise UserError(
                    _('Only documents past their expiry date can be '
                      'force-expired.'))
            self._write_history(doc, 'expired')
            doc.message_post(body=_('Document expired.'))

    @api.model
    def _write_history(self, doc, action):
        vals = {
            'document_id': doc.id,
            'action': action,
            'action_date': fields.Datetime.now(),
            'old_expiry_date': doc.expiry_date,
            'new_expiry_date': doc.expiry_date,
            'user_id': self.env.user.id,
        }
        self.env['sf.compliance.history'].create(vals)

    @api.model
    def _check_expiry_alerts(self):
        docs = self.search([('published', '=', True)])
        for doc in docs:
            doc.invalidate_recordset()
            if doc.state == 'expiring' and doc.responsible_id:
                existing = doc.activity_ids.filtered(
                    lambda a: a.summary ==
                    _('Document expiring: %s') % doc.name)
                if not existing:
                    doc.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Document expiring: %s') % doc.name,
                        note=_('The document "%s" expires on %s. Please '
                               'renew it.') % (doc.name, doc.expiry_date),
                        user_id=doc.responsible_id.id,
                        date_deadline=doc.expiry_date,
                    )
            elif doc.state == 'expired':
                if not doc.history_ids.filtered(
                        lambda h: h.action == 'expired'):
                    self._write_history(doc, 'expired')

    def unlink(self):
        for doc in self:
            if doc.state in ('active', 'expiring', 'expired'):
                raise UserError(
                    _('A published document cannot be deleted. Archive '
                      'it instead.'))
        return super().unlink()


class ComplianceHistory(models.Model):
    _name = 'sf.compliance.history'
    _description = 'Compliance Document History'
    _order = 'action_date desc'

    document_id = fields.Many2one('sf.compliance.document',
                                  string='Document',
                                  ondelete='cascade', required=True)
    action = fields.Selection([
        ('created', 'Created'),
        ('renewed', 'Renewed'),
        ('expired', 'Expired'),
        ('updated', 'Updated'),
    ], string='Action', required=True)
    action_date = fields.Datetime(string='Action Date', required=True)
    old_expiry_date = fields.Date(string='Old Expiry Date')
    new_expiry_date = fields.Date(string='New Expiry Date')
    user_id = fields.Many2one('res.users', string='User')
    notes = fields.Text(string='Notes')


class ComplianceRenewWizard(models.TransientModel):
    _name = 'sf.compliance.renew.wizard'
    _description = 'Compliance Document Renewal'

    document_id = fields.Many2one('sf.compliance.document',
                                  string='Document', required=True,
                                  readonly=True)
    new_expiry_date = fields.Date(string='New Expiry Date',
                                  required=True)
    issuer = fields.Char(string='Issuer')
    notes = fields.Text(string='Notes')

    def action_renew(self):
        self.ensure_one()
        doc = self.document_id
        if self.new_expiry_date <= fields.Date.today():
            raise UserError(
                _('The new expiry date must be in the future.'))
        old = doc
        new = self.env['sf.compliance.document'].create({
            'name': old.name,
            'document_type_id': old.document_type_id.id,
            'issuer': self.issuer or old.issuer,
            'partner_id': old.partner_id.id,
            'issue_date': fields.Date.today(),
            'expiry_date': self.new_expiry_date,
            'responsible_id': old.responsible_id.id,
            'renewal_of_id': old.id,
            'company_id': old.company_id.id,
            'notes': old.notes,
        })
        old.renewed_by_id = new.id
        self.env['sf.compliance.history'].create({
            'document_id': new.id,
            'action': 'renewed',
            'action_date': fields.Datetime.now(),
            'old_expiry_date': old.expiry_date,
            'new_expiry_date': self.new_expiry_date,
            'user_id': self.env.user.id,
            'notes': self.notes,
        })
        new.published = True
        old.active = False
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.compliance.document',
            'res_id': new.id,
            'view_mode': 'form',
        }