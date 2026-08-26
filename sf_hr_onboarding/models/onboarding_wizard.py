# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OnboardingGenerateWizard(models.TransientModel):
    _name = 'sf.onboarding.generate.wizard'
    _description = 'Generate Onboarding/Offboarding Program'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    program_type = fields.Selection([
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding'),
    ], string='Type', default='onboarding', required=True)
    template_id = fields.Many2one('sf.onboarding.template',
                                  string='Template')
    key_date = fields.Date(string='Key Date')

    @api.onchange('program_type', 'employee_id')
    def _onchange_template(self):
        self.template_id = False
        if self.employee_id and self.program_type == 'onboarding':
            self.template_id = self.employee_id.company_id.\
                sf_onboarding_default_template
        elif self.employee_id and self.program_type == 'offboarding':
            self.template_id = self.employee_id.company_id.\
                sf_offboarding_default_template

    def action_generate(self):
        self.ensure_one()
        if not self.template_id:
            raise UserError(_('A template is required to generate the '
                              'program.'))
        program = self.env['sf.onboarding.program'].create({
            'employee_id': self.employee_id.id,
            'program_type': self.program_type,
            'template_id': self.template_id.id,
            'key_date': self.key_date or fields.Date.today(),
        })
        program._generate_tasks()
        program.action_start()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.onboarding.program',
            'res_id': program.id,
            'view_mode': 'form',
        }