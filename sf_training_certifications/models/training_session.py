# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TrainingSession(models.Model):
    _name = 'sf.training.session'
    _description = 'Training Session'
    _inherit = ['mail.thread']
    _order = 'date_start desc'

    training_id = fields.Many2one('sf.training', string='Training',
                                  required=True, ondelete='cascade')
    name = fields.Char(string='Name')
    date_start = fields.Datetime(string='Start', required=True)
    date_end = fields.Datetime(string='End', required=True)
    trainer_id = fields.Many2one('res.partner', string='Trainer')
    location = fields.Char(string='Location')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    registration_ids = fields.One2many('sf.training.registration',
                                       'session_id',
                                       string='Registrations')
    attendee_count = fields.Integer(string='Attendees',
                                    compute='_compute_attendee_count',
                                    store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    @api.onchange('training_id', 'date_start', 'date_end')
    def _onchange_name(self):
        if self.training_id and self.date_start:
            self.name = '%s - %s' % (
                self.training_id.name,
                self.date_start.strftime('%d/%m/%Y'))

    @api.depends('registration_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = len(session.registration_ids)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for session in self:
            if session.date_end < session.date_start:
                raise UserError(
                    _('The end date cannot be before the start date.'))

    def action_plan(self):
        for session in self:
            if session.state != 'draft':
                raise UserError(
                    _('Only draft sessions can be planned.'))
            if not session.registration_ids:
                raise UserError(
                    _('A session must have registrations to be planned.'))
            session.state = 'planned'

    def action_done(self):
        for session in self:
            if session.state != 'planned':
                raise UserError(
                    _('Only planned sessions can be marked as done.'))
            if not session.registration_ids:
                raise UserError(
                    _('A session must have registrations to be done.'))
            session.state = 'done'

    def action_cancel(self):
        for session in self:
            if session.state == 'done':
                raise UserError(
                    _('A done session cannot be cancelled.'))
            session.state = 'cancelled'

    def action_issue_certificates(self):
        view = self.env.ref(
            'sf_training_certifications.certification_issue_wizard_form')
        return {
            'name': _('Issue Certificates'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.certification.issue.wizard',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'context': {'default_session_id': self.id},
        }

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.certification.issue.wizard'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiration_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiration_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.expiration_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave2 ---
class _Wave2CertScan(models.Model):
    _inherit = 'sf.employee.certification'

    @api.model
    def action_scan_expirations(self):
        """Flip state to expiring/expired per company alert window and
        notify the employee's manager via chatter on the certification."""
        icp = self.env['ir.config_parameter'].sudo()
        alert_days = int(icp.get_param(
            'sf_training_certifications.alert_days',
            str(self.env.company.sf_cert_alert_days or 30)))
        today = fields.Date.context_today(self)
        from dateutil.relativedelta import relativedelta as rd
        soon = today + rd(days=alert_days)
        expired = self.search([
            ('expiration_date', '!=', False),
            ('expiration_date', '<', today),
            ('state', 'in', ('draft', 'active', 'expiring'))])
        expiring = self.search([
            ('expiration_date', '>=', today),
            ('expiration_date', '<=', soon),
            ('state', 'in', ('draft', 'active'))])
        expired.write({'state': 'expired'})
        expiring.write({'state': 'expiring'})
        for cert in expiring:
            mgr = cert.employee_id.parent_id.user_id
            cert.message_post(body=_(
                'Certification expires on %s (%s days). Manager notified: %s')
                % (cert.expiration_date, alert_days,
                   mgr.name if mgr else '-'))
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('Certifications'),
                       'message': _('%d expired, %d expiring soon.')
                       % (len(expired), len(expiring)),
                       'type': 'success'},
        }
