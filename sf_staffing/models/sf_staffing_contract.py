# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfStaffingContract(models.Model):
    _name = 'sf.staffing.contract'
    _description = 'Staffing Contract'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    mission_id = fields.Many2one('sf.staffing.mission', string='Mission', required=True, ondelete='cascade')
    candidate_id = fields.Many2one('sf.staffing.candidate', string='Candidate', required=True)
    client_id = fields.Many2one('sf.staffing.client', string='Client', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    hourly_rate = fields.Monetary(string='Hourly Rate', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.contract')
        return super().create(vals_list)

    def write(self, vals):
        if 'hourly_rate' in vals and any(contract.state != 'draft' for contract in self):
            if not self.env.user.has_group('sf_staffing.group_sf_staffing_manager'):
                raise UserError(_('Only a staffing manager can modify contractual rates.'))
        return super().write(vals)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})