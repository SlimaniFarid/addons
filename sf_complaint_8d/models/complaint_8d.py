# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Complaint8d(models.Model):
    _name = 'sf.complaint.8d.complaint_8d'
    _description = 'Complaint_8D'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    product_id = fields.Many2one(comodel_name='product.product', ondelete='restrict')
    problem_description = fields.Html(string='Problem Description')
    root_cause = fields.Html(string='Root Cause')
    corrective_action = fields.Html(string='Corrective Action')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('d1_team', 'D1 - Team'),
        ('d2_problem', 'D2 - Problem Description'),
        ('d3_containment', 'D3 - Containment'),
        ('d4_root_cause', 'D4 - Root Cause'),
        ('d5_corrective', 'D5 - Corrective Actions'),
        ('d6_validate', 'D6 - Validate Effectiveness'),
        ('d7_prevent', 'D7 - Prevent Recurrence'),
        ('d8_closed', 'D8 - Close & Recognise'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.complaint.8d.complaint_8d') or _('New')
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
    _inherit = 'sf.complaint.8d.complaint_8d'

    active = fields.Boolean(string='Active', default=True)
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

