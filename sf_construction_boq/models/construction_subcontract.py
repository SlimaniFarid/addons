from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ConstructionSubcontract(models.Model):
    _name = 'construction.subcontract'
    _description = 'Subcontract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    project_id = fields.Many2one('project.project', string='Project', ondelete='restrict', required=True, tracking=True)
    contractor_id = fields.Many2one('res.partner', string='Contractor', ondelete='restrict', required=True, tracking=True)
    contract_amount = fields.Monetary(string='Contract Amount', currency_field='currency_id', tracking=True)
    retention_rate = fields.Float(string='Retention Rate (%)', default=10.0, tracking=True)
    advance_amount = fields.Monetary(string='Advance', currency_field='currency_id', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    certificate_ids = fields.One2many('construction.payment.certificate', 'subcontract_id', string='Payment Certificates')
    amount_certified = fields.Monetary(string='Certified', currency_field='currency_id',
                                       compute='_compute_amount_certified', store=True)

    @api.depends('certificate_ids.amount_to_pay')
    def _compute_amount_certified(self):
        for sub in self:
            sub.amount_certified = sum(sub.certificate_ids.mapped('amount_to_pay'))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.subcontract') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for sub in self:
            if sub.state != 'draft':
                raise UserError(_('Only a draft subcontract can be confirmed.'))
            sub.state = 'confirmed'

    def action_start(self):
        for sub in self:
            if sub.state != 'confirmed':
                raise UserError(_('Only a confirmed subcontract can be started.'))
            sub.state = 'in_progress'

    def action_close(self):
        for sub in self:
            sub.state = 'closed'

    def action_cancel(self):
        for sub in self:
            if sub.state in ('closed',):
                raise UserError(_('A closed subcontract cannot be cancelled.'))
            sub.state = 'cancelled'

    def action_create_certificate(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'in_progress'):
            raise UserError(_('The subcontract must be confirmed or in progress to create a payment certificate.'))
        certificate = self.env['construction.payment.certificate'].create({
            'subcontract_id': self.id,
            'project_id': self.project_id.id,
            'contractor_id': self.contractor_id.id,
            'retention_rate': self.retention_rate,
        })
        return {
            'name': _('Payment Certificate'),
            'type': 'ir.actions.act_window',
            'res_model': 'construction.payment.certificate',
            'view_mode': 'form',
            'res_id': certificate.id,
            'target': 'current',
        }

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'construction.boq'

    active = fields.Boolean(string='Active', default=True)
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'construction.boq'

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
