# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseRequisitionSf(models.Model):
    _name = 'sf.purchase.requisition.purchase.requisition.sf'
    _description = 'Purchase Requisition Sf'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Char(string='Name', required=True)
    requested_by = fields.Many2one(default='current', comodel_name='res.users', ondelete='restrict')
    department_id = fields.Many2one(comodel_name='hr.department', ondelete='restrict')
    budget_check = fields.Boolean(string='Budget Check', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)
    line_ids = fields.One2many('requisition.line', 'Lines', string='Line Ids')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.purchase.requisition.purchase.requisition.sf') or _('New')
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

