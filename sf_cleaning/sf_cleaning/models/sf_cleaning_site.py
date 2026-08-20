# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfCleaningSite(models.Model):
    _name = 'sf.cleaning.site'
    _description = 'Cleaning Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Client', ondelete='restrict', required=True)
    address_id = fields.Many2one(
        'res.partner', string='Delivery address', ondelete='set null')
    area_m2 = fields.Float(string='Area (m2)')
    manager_id = fields.Many2one(
        'res.users', string='Team leader', default=lambda self: self.env.user)
    schedule_ids = fields.One2many(
        'sf.cleaning.schedule', 'site_id', string='Schedules')
    validated_intervention_count = fields.Integer(
        string='Validated interventions', compute='_compute_validated_intervention_count',
        store=True)
    notes = fields.Text(string='Notes')

    @api.depends('schedule_ids.line_ids.state', 'schedule_ids.state')
    def _compute_validated_intervention_count(self):
        for site in self:
            site.validated_intervention_count = len(
                site.schedule_ids.line_ids.filtered(
                    lambda l: l.state == 'done' and l.schedule_id.state in (
                        'validated', 'invoiced')))