# -*- coding: utf-8 -*-
from odoo import fields, models, _, api
from odoo.exceptions import UserError


class ItAssignment(models.Model):
    _name = 'sf.it.assignment'
    _description = 'IT Asset Assignment'
    _order = 'date_from desc'

    asset_id = fields.Many2one('sf.it.asset', string='Asset',
                               required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To')
    state = fields.Selection([
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='active')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

    @api.constrains('asset_id', 'state')
    def _check_unique_active(self):
        for assignment in self:
            if assignment.state == 'active':
                duplicate = self.env['sf.it.assignment'].search([
                    ('asset_id', '=', assignment.asset_id.id),
                    ('state', '=', 'active'),
                    ('id', '!=', assignment.id),
                ])
                if duplicate:
                    raise UserError(
                        _('This asset already has an active assignment.'))

    @api.constrains('asset_id', 'state')
    def _check_asset_state(self):
        for assignment in self:
            if assignment.state == 'active':
                if assignment.asset_id.state != 'in_stock':
                    raise UserError(
                        _('Only assets in stock can be assigned.'))

    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.state == 'active':
                rec.asset_id.write({'state': 'assigned'})
        return records

    def write(self, vals):
        result = super().write(vals)
        for rec in self:
            rec.asset_id._compute_assignment()
            if rec.state == 'active':
                rec.asset_id.write({'state': 'assigned'})
            else:
                active = rec.asset_id._get_active_assignment()
                if not active:
                    rec.asset_id.write({'state': 'in_stock'})
        return result

    def action_close(self):
        for rec in self:
            rec.write({
                'state': 'closed',
                'date_to': rec.date_to or fields.Date.today(),
            })
        return True