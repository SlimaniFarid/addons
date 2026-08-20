# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models


class SfParkingReportWizard(models.TransientModel):
    _name = 'sf.parking.report.wizard'
    _description = 'Parking Reports Wizard'

    site_id = fields.Many2one('sf.parking.site', string='Site')
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    def _ticket_domain(self):
        domain = [('state', '=', 'paid')]
        if self.site_id:
            domain.append(('site_id', '=', self.site_id.id))
        if self.date_from:
            domain.append(('entry_datetime', '>=', self.date_from))
        if self.date_to:
            domain.append(('entry_datetime', '<', self.date_to + timedelta(days=1)))
        return domain

    def action_revenue_report(self):
        tickets = self.env['sf.parking.ticket'].search(self._ticket_domain())
        return self.env.ref('sf_parking_management.action_report_revenue').report_action(tickets)

    def action_occupancy_report(self):
        sites = self.site_id or self.env['sf.parking.site'].search([])
        return self.env.ref('sf_parking_management.action_report_occupancy').report_action(sites)