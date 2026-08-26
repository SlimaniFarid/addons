# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SlaTier(models.Model):
    _name = 'sf.sla.tier'
    _description = 'SLA Tier'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    response_hours = fields.Integer(string='Response Time (hours)',
                                    required=True, default=4)
    resolution_hours = fields.Integer(string='Resolution Time (hours)',
                                      required=True, default=24)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Tier code must be unique.'),
    ]


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.service.contract'

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
