# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PromoRule(models.Model):
    _name = 'sf.promotional.pricing.engine.promo.rule'
    _description = 'Promo Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Char(string='Name', required=True)
    product_tmpl_ids = fields.Many2many('product.template', string='Product Tmpl Ids')
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)
    discount_pct = fields.Float(string='Discount Pct', default=0.0)
    fixed_price = fields.Monetary(string='Fixed Price', currency_field='currency_id', currency_field='currency_id')
    min_qty = fields.Float(string='Min Qty', default=1.0)
    margin_floor_pct = fields.Float(string='Margin Floor Pct', default=0.0)
    active = fields.Boolean(string='Active', default='True')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.promotional.pricing.engine.promo.rule') or _('New')
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

