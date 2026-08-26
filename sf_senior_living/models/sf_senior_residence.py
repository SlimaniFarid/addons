# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfSeniorResidence(models.Model):
    _name = 'sf.senior.residence'
    _description = 'Senior Residence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Residence Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    capacity = fields.Integer(string='Total Capacity')
    manager_id = fields.Many2one('res.users', string='Residence Manager')
    state = fields.Selection([
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('closed', 'Closed'),
    ], string='Status', default='active', tracking=True)
    resident_ids = fields.One2many('sf.senior.resident', 'residence_id',
                                   string='Residents')
    resident_count = fields.Integer(string='Residents',
                                    compute='_compute_resident_count',
                                    store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    @api.depends('resident_ids')
    def _compute_resident_count(self):
        for rec in self:
            rec.resident_count = len(rec.resident_ids)

    def action_close(self):
        self.write({'state': 'closed'})

    def action_reopen(self):
        self.write({'state': 'active'})
