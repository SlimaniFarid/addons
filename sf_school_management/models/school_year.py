# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SchoolYear(models.Model):
    _name = 'sf.school.year'
    _description = 'School Year'
    _order = 'date_from desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Year', required=True, index=True)
    date_from = fields.Date(string='Start date')
    date_to = fields.Date(string='End date')
    state = fields.Selection([
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='active', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.year')
        return super().create(vals)

    def action_close_year(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active years can be closed.'))
        self.state = 'closed'

    def action_reopen_year(self):
        self.ensure_one()
        if self.state != 'closed':
            raise UserError(_('Only closed years can be reopened.'))
        self.state = 'active'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.school.absence'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
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
                vals['Deadline'] = str(rec.due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

