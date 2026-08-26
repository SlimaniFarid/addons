# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class QualityInspection(models.Model):
    _name = 'sf.quality.inspection.quality.inspection'
    _description = 'Quality Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.Many2one('sf.quality_inspection.inspection.plan', string='Plan Id', required=True)
    picking_id = fields.Many2one('stock.picking', string='Picking Id')
    result = fields.Selection([('pass','Pass'),('fail','Fail'),('pending','Pending')], string='Result', default='pending tracking', tracking=True)
    inspector_id = fields.Many2one('res.users', string='Inspector Id', default='current')
    notes = fields.Html(string='Notes')
    photo_ids = fields.Many2many('ir.attachment', string='Photo Ids')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.quality.inspection.inspection.plan'

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
    _inherit = 'sf.quality.inspection.inspection.plan'

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
