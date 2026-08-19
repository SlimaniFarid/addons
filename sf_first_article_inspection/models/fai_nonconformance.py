# -*- coding: utf-8 -*-
from odoo import fields, models, _


class FAINonconformance(models.Model):
    _name = 'sf.fai.nonconformance'
    _description = 'FAI Non-conformance'
    _order = 'date desc, id desc'

    report_id = fields.Many2one('sf.fai.report', string='FAI Report', required=True, ondelete='cascade')
    characteristic_id = fields.Many2one('sf.fai.characteristic', string='Characteristic')
    nc_number = fields.Char(string='NC Number', required=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    description = fields.Text(string='Description', required=True)
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', default='minor', required=True)
    disposition = fields.Selection([
        ('use_as_is', 'Use As Is'),
        ('rework', 'Rework'),
        ('scrap', 'Scrap'),
        ('return_to_supplier', 'Return to Supplier'),
    ], string='Disposition')
    disposition_rationale = fields.Text(string='Disposition Rationale')
    corrective_action = fields.Text(string='Corrective Action')
    preventive_action = fields.Text(string='Preventive Action')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    target_date = fields.Date(string='Target Completion Date')
    closed_date = fields.Date(string='Closed Date')
    state = fields.Selection([
        ('open', 'Open'),
        ('dispositioned', 'Dispositioned'),
        ('closed', 'Closed'),
    ], string='Status', default='open')

    def action_disposition(self):
        self.write({'state': 'dispositioned'})

    def action_close(self):
        self.write({'state': 'closed', 'closed_date': fields.Date.today()})