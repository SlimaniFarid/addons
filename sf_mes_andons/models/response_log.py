# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AndonResponseLog(models.Model):
    _name = 'sf.andon.response.log'
    _description = 'Andon Response Log'
    _order = 'create_date desc'

    call_id = fields.Many2one('sf.andon.call', string='Andon Call', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    action = fields.Selection([
        ('acknowledged', 'Acknowledged'),
        ('started', 'Started Work'),
        ('updated', 'Status Updated'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
        ('commented', 'Comment Added'),
        ('reassigned', 'Reassigned'),
    ], string='Action', required=True)
    comment = fields.Text(string='Comment')
    previous_state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Previous State')
    new_state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='New State')
    create_date = fields.Datetime(string='Timestamp', readonly=True)


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.andon.call'

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
