# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonStaff(models.Model):
    _name = 'sf.salon.staff'
    _description = 'Salon Staff'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='restrict')
    commission_rate = fields.Float(string='Commission Rate (%)')
    active = fields.Boolean(string='Active', default=True)
    service_ids = fields.Many2many('sf.salon.service', string='Services')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def _check_rate_edit(self, vals):
        if 'commission_rate' in vals and not self.env.user.has_group('sf_salon_beauty.group_sf_salon_manager'):
            raise UserError(_('Only a salon manager can set commission rates.'))

    def _get_default_commission_rate(self):
        return float(self.env['ir.config_parameter'].sudo().get_param('sf_salon_beauty.default_commission_rate', '10.0'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.staff')
            self._check_rate_edit(vals)
            if 'commission_rate' not in vals:
                vals['commission_rate'] = self._get_default_commission_rate()
        return super().create(vals_list)

    def write(self, vals):
        if 'commission_rate' in vals:
            self._check_rate_edit(vals)
        return super().write(vals)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.salon.activity.mixin'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.expiration_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.salon.activity.mixin'

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
