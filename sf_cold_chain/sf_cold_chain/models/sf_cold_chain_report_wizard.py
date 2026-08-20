# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfColdChainReportWizard(models.TransientModel):
    _name = 'sf.cold.chain.report.wizard'
    _description = 'Cold Chain Report Wizard'

    site_id = fields.Many2one('sf.cold.site', string='Cold Storage Site')
    trip_id = fields.Many2one('sf.cold.trip', string='Cold Transport Trip')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    def action_print_report(self):
        self.ensure_one()
        if not self.site_id and not self.trip_id:
            raise UserError(_('Please select a site or a trip.'))
        domain = []
        if self.site_id:
            domain = [('site_id', '=', self.site_id.id)]
        elif self.trip_id:
            domain = [('trip_id', '=', self.trip_id.id)]
        if self.date_from:
            domain.append(('recorded_at', '>=', self.date_from))
        if self.date_to:
            domain.append(('recorded_at', '<=', self.date_to))
        readings = self.env['sf.cold.reading'].search(domain, order='recorded_at asc')
        return self.env.ref('sf_cold_chain.action_report_cold_log').report_action(readings)