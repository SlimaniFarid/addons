# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CrecheRoom(models.Model):
    _name = 'sf.creche.room'
    _description = 'Creche Room'
    _order = 'name'

    name = fields.Char(string='Room', required=True, index=True)
    capacity = fields.Integer(string='Capacity', required=True)
    educator_ids = fields.Many2many('res.users', string='Educators')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True)
    enrollment_ids = fields.One2many('sf.creche.enrollment', 'room_id',
                                     string='Enrollments')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.room')
        return super().create(vals)

    def action_done(self):
        self.ensure_one()
        self.state = 'done'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.creche.attendance'

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

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

