# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfPolicyAcknowledgment(models.Model):
    _name = 'sf.policy.acknowledgment'
    _description = 'Policy Acknowledgment'
    _order = 'policy_id asc, employee_id asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    policy_id = fields.Many2one(
        'sf.policy', string='Policy', required=True, ondelete='cascade')
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True)
    acknowledged_date = fields.Date(string='Acknowledged On', copy=False)
    acknowledged_by = fields.Many2one(
        'res.users', string='Acknowledged By', copy=False)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
    ], string='Status', default='pending', copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('acknowledgment_unique_policy_employee',
         'UNIQUE (policy_id, employee_id)',
         'An employee can only have one acknowledgment per policy.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.policy.acknowledgment')
            if vals.get('policy_id') and not vals.get('company_id'):
                policy = self.env['sf.policy'].browse(vals['policy_id'])
                vals['company_id'] = policy.company_id.id
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals and not self.env.context.get(
                'sf_policy_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        if self.filtered(lambda a: a.state == 'acknowledged') \
                and not self.env.context.get('sf_policy_bypass_state'):
            raise UserError(_('An acknowledged acknowledgment cannot be modified.'))
        return super().write(vals)

    def action_acknowledge(self):
        for record in self:
            if record.state != 'pending':
                raise UserError(_('Only pending acknowledgments can be acknowledged.'))
            if record.policy_id.state != 'published':
                raise UserError(_('Only acknowledgments of a published policy can be collected.'))
            record.with_context(sf_policy_bypass_state=True).write({
                'state': 'acknowledged',
                'acknowledged_date': fields.Date.context_today(record),
                'acknowledged_by': self.env.user.id,
            })