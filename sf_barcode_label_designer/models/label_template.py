# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LabelTemplate(models.Model):
    _name = 'sf.barcode.label.designer.label.template'
    _description = 'Label Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Char(string='Name', required=True)
    label_width_mm = fields.Float(string='Label Width Mm', default=50)
    label_height_mm = fields.Float(string='Label Height Mm', default=30)
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('active', 'Active'),
        ('archived', 'Archived'), ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)
    barcode_type = fields.Selection([
        ('code128', 'Code 128'), ('ean13', 'EAN-13'), ('ean8', 'EAN-8'),
        ('upca', 'UPC-A'), ('qr', 'QR Code'), ('datamatrix', 'Data Matrix'),
        ], string='Barcode Type', default='code128', required=True)
    output_format = fields.Selection([
        ('pdf', 'PDF'), ('png', 'PNG'), ('zpl', 'ZPL'),
        ], string='Output Format', default='pdf', required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.barcode.label.designer.label.template') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()
    
    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.barcode.label.designer.label.print.batch'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.barcode.label.designer.label.print.batch'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
