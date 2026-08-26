from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaTherapistSchedule(models.Model):
    _name = 'sf.spa.therapist.schedule'
    _description = 'Therapist Weekly Schedule'
    _inherit = ['sf.spa.company.mixin']
    _order = 'day_of_week, start_time'

    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', required=True, ondelete='cascade')
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True, help='Start time in hours (e.g., 9.0 for 9:00, 14.5 for 14:30)')
    end_time = fields.Float(string='End Time', required=True, help='End time in hours')
    resource_ids = fields.Many2many(
        'sf.spa.resource',
        'sf_spa_therapist_schedule_resource_rel',
        'schedule_id',
        'resource_id',
        string='Preferred Resources'
    )

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for record in self:
            if record.start_time < 0 or record.start_time >= 24:
                raise ValidationError(_('Start time must be between 0 and 24.'))
            if record.end_time < 0 or record.end_time > 24:
                raise ValidationError(_('End time must be between 0 and 24.'))
            if record.start_time >= record.end_time:
                raise ValidationError(_('Start time must be before end time.'))

    @api.constrains('therapist_id', 'day_of_week', 'start_time', 'end_time')
    def _check_overlap(self):
        for record in self:
            overlapping = self.search([
                ('therapist_id', '=', record.therapist_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if overlapping:
                raise ValidationError(_('Schedule overlaps with existing schedule for this therapist on this day.'))

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf_spa_wellness.activity.mixin'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf_spa_wellness.activity.mixin'

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
