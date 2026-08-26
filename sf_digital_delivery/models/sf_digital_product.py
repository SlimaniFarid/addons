# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfDigitalProduct(models.Model):
    _name = 'sf.digital.product'
    _description = 'Digital Product'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.digital.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.template', string='Saleable Product', required=True)
    delivery_type = fields.Selection([
        ('license_key', 'License Key'),
        ('download', 'Download Link'),
    ], string='Delivery Type', required=True, default='license_key')
    key_format = fields.Char(string='Key Format', help='License key format, e.g. XXXX-XXXX-XXXX')
    max_activations = fields.Integer(string='Max Activations', default=1)
    validity_days = fields.Integer(string='Link Validity (days)', default=30)
    file_binary = fields.Binary(string='File to Download')
    file_name = fields.Char(string='File Name')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.digital.product')
            if not vals.get('key_format'):
                vals['key_format'] = self.env['ir.config_parameter'].sudo().get_param(
                    'sf_digital_delivery.default_key_format', 'XXXX-XXXX-XXXX')
            if not vals.get('validity_days'):
                default_validity = self.env['ir.config_parameter'].sudo().get_param(
                    'sf_digital_delivery.default_validity_days', '30')
                vals['validity_days'] = int(default_validity)
        return super().create(vals_list)

    def write(self, vals):
        if 'delivery_type' in vals and 'key_format' not in vals:
            for record in self:
                if record.delivery_type == 'license_key' and not record.key_format:
                    vals['key_format'] = self.env['ir.config_parameter'].sudo().get_param(
                        'sf_digital_delivery.default_key_format', 'XXXX-XXXX-XXXX')
                    break
        return super().write(vals)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.digital.delivery'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('download_expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.download_expiry_date
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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.digital.delivery'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
