# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ShopFloorEntry(models.Model):
    _name = 'sf.shop.floor.terminal.shop.floor.entry'
    _description = 'Shop Floor Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    employee_id = fields.Many2one(required=True, comodel_name='hr.employee', ondelete='restrict')
    workorder_id = fields.Many2one(comodel_name='mrp.workorder', ondelete='restrict')
    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time')
    qty_produced = fields.Float(string='Qty Produced', default=0.0)
    qty_scrap = fields.Float(string='Qty Scrap', default=0.0)
    state = fields.Selection([
        ('draft', 'Draft'), ('running', 'Running'), ('paused', 'Paused'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled'),
        ], string='Status', default='running', copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.shop.floor.terminal.shop.floor.entry') or _('New')
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
    _inherit = 'sf.shop.floor.terminal.shop.floor.entry'

    active = fields.Boolean(string='Active', default=True)
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.shop.floor.terminal.shop.floor.entry'

    def action_refresh_business(self):
        """Pull active MO count and average yield."""
        Mos = self.env['mrp.production']
        active = Mos.search([('state', 'in', ('confirmed', 'progress'))])
        done = Mos.search([('state', '=', 'done')], limit=50)
        yields = [(mo.qty_produced / mo.product_qty * 100)
                  for mo in done if mo.product_qty]
        avg_yield = sum(yields) / len(yields) if yields else 0.0
        for rec in self:
            rec.message_post(body=_(
                '{a} active MO(s), avg yield {y:.1f}% on last {d} done.')
                .format(a=len(active), y=avg_yield, d=len(done)))
        return True
