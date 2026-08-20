# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfStaffingNeed(models.Model):
    _name = 'sf.staffing.need'
    _description = 'Staffing Need'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    client_id = fields.Many2one('sf.staffing.client', string='Client', required=True, ondelete='cascade')
    job_title = fields.Char(string='Job Title', required=True)
    required_skills = fields.Text(string='Required Skills')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    state = fields.Selection([
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)
    mission_ids = fields.One2many('sf.staffing.mission', 'need_id', string='Missions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.need')
        return super().create(vals_list)

    def action_open(self):
        self.state = 'open'

    def action_assigned(self):
        self.state = 'assigned'

    def action_fill(self):
        self.state = 'filled'

    def action_cancel(self):
        self.state = 'cancelled'