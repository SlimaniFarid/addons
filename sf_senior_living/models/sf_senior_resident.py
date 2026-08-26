# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfSeniorResident(models.Model):
    _name = 'sf.senior.resident'
    _description = 'Senior Resident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Full Name', required=True)
    residence_id = fields.Many2one('sf.senior.residence',
                                   string='Residence', required=True,
                                   ondelete='restrict')
    partner_id = fields.Many2one('res.partner', string='Related Contact')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    room_number = fields.Char(string='Room Number')
    gir_level = fields.Integer(string='GIR Level (1-6)',
                               help='Autonomy level: 1=dependent, '
                                    '6=autonomous')
    admission_date = fields.Date(string='Admission Date',
                                 default=fields.Date.today)
    discharge_date = fields.Date(string='Discharge Date')
    emergency_contact = fields.Char(string='Emergency Contact')
    medical_notes = fields.Html(string='Medical Notes')
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('deceased', 'Deceased'),
    ], string='Status', default='admitted', tracking=True)
    company_id = fields.Many2one(related='residence_id.company_id',
                                 store=True)

    @api.constrains('gir_level')
    def _check_gir_level(self):
        for rec in self:
            if rec.gir_level and not (1 <= rec.gir_level <= 6):
                raise _('%s: GIR level must be between 1 and 6.') % rec.name

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf_senior_living.activity.mixin'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
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
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf_senior_living.activity.mixin'

    def action_refresh_business(self):
        """Pull open / overdue amounts for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            moves = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', partner.id)])
            open_amt = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
            ).mapped('amount_residual'))
            today = fields.Date.context_today(rec)
            overdue = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
                and m.invoice_date_due
                and m.invoice_date_due < today
            ).mapped('amount_residual'))
            rec.message_post(body=_(
                'Open: {o:.2f}, Overdue: {d:.2f} '
                '({c} posted invoice(s)).').format(
                o=open_amt, d=overdue, c=len(moves)))
        return True
