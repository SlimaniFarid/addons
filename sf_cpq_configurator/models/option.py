# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CpqOption(models.Model):
    _name = 'sf.cpq.option'
    _description = 'CPQ Option'
    _rec_name = 'name'
    _order = 'sequence, name'

    attribute_id = fields.Many2one('sf.cpq.attribute', string='Attribute',
                                   required=True, ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    price_adjust = fields.Float(string='Price Adjustment', default=0.0,
                                help="Added to or deducted from the base "
                                     "product price.")
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(attribute_id, code)',
         'Option code must be unique per attribute.'),
    ]


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.cpq.attribute'

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
