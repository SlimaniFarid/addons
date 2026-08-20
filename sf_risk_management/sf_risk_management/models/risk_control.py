# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RiskControl(models.Model):
    _name = 'sf.risk.control'
    _description = 'Risk Control'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference')
    category = fields.Selection([
        ('preventive', 'Preventive'),
        ('detective', 'Detective'),
        ('corrective', 'Corrective'),
    ], string='Category', default='preventive')
    frequency = fields.Selection([
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Frequency', default='monthly')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    risk_ids = fields.Many2many('sf.risk',
                                'sf_risk_control_rel', 'control_id',
                                'risk_id', string='Risks')
    last_test_date = fields.Date(string='Last Test Date',
                                 compute='_compute_last_test', store=True)
    last_test_result = fields.Selection([
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('not_tested', 'Not Tested'),
    ], string='Last Result', compute='_compute_last_test', store=True)
    tests = fields.One2many('sf.risk.control.test', 'control_id',
                            string='Test History')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.depends('tests.test_date', 'tests.result')
    def _compute_last_test(self):
        for control in self:
            if control.tests:
                last = control.tests.sorted(
                    key=lambda t: t.test_date, reverse=True)[0]
                control.last_test_date = last.test_date.date() \
                    if last.test_date else False
                control.last_test_result = last.result
            else:
                control.last_test_date = False
                control.last_test_result = 'not_tested'

    def action_run_test(self):
        self.ensure_one()
        return {
            'name': _('Run Test'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.risk.control.test',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_control_id': self.id},
        }


class RiskControlTest(models.Model):
    _name = 'sf.risk.control.test'
    _description = 'Risk Control Test'
    _order = 'test_date desc'

    control_id = fields.Many2one('sf.risk.control', string='Control',
                                 ondelete='cascade', required=True)
    test_date = fields.Datetime(string='Test Date',
                                default=fields.Datetime.now,
                                required=True)
    tested_by = fields.Many2one('res.users', string='Tested By',
                                default=lambda self: self.env.user)
    result = fields.Selection([
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ], string='Result', required=True)
    notes = fields.Text(string='Notes')
    action_id = fields.Many2one('sf.risk.action',
                                string='Linked Action')

    @api.constrains('result', 'action_id')
    def _check_failed_action(self):
        for test in self:
            if test.result == 'failed' and not test.action_id:
                raise UserError(
                    _('A failed test requires a linked treatment '
                      'action.'))

    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.control_id.message_post(body=_(
                'Test recorded: %s.') % dict(
                    record._fields['result'].selection).get(record.result))
        return records