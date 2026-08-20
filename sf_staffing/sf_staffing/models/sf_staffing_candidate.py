# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfStaffingCandidate(models.Model):
    _name = 'sf.staffing.candidate'
    _description = 'Staffing Candidate'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.staffing.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    skills = fields.Text(string='Skills')
    availability = fields.Selection([
        ('immediate', 'Immediate'),
        ('one_week', 'Within One Week'),
        ('one_month', 'Within One Month'),
        ('none', 'Not Available'),
    ], string='Availability', default='immediate')
    desired_job = fields.Char(string='Desired Job')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('on_mission', 'On Mission'),
        ('unavailable', 'Unavailable'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)
    mission_ids = fields.One2many('sf.staffing.mission', 'candidate_id', string='Missions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.candidate')
        return super().create(vals_list)

    def action_draft(self):
        self.state = 'draft'

    def action_available(self):
        self.state = 'available'

    def action_assigned(self):
        self.state = 'assigned'

    def action_on_mission(self):
        self.state = 'on_mission'

    def action_unavailable(self):
        self.state = 'unavailable'