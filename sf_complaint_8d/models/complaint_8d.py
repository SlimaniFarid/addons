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
    partner_id = fields.Many2one('res.partner', string='Partner Id')
    product_id = fields.Many2one('product.product', string='Product Id')
    problem_description = fields.Html(string='Problem Description')
    root_cause = fields.Html(string='Root Cause')
    corrective_action = fields.Html(string='Corrective Action')
    state = fields.Selection([('d1_team','D1 Team'),('d2_problem','D2 Problem'),('d3_interim','D3 Interim'),('d4_root','D4 Root Cause'),('d5_actions','D5 Actions'),('d6_implemented','D6 Implemented'),('d7_prevented','D7 Prevented'),('d8_closed','D8 Closed')], string='State', default='d1_team tracking', tracking=True)

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

