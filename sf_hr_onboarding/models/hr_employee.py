# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class OnboardingHrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_onboarding_program_ids = fields.One2many(
        'sf.onboarding.program', 'employee_id', string='Programs')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._auto_generate_onboarding()
        return records

    def _auto_generate_onboarding(self):
        self.ensure_one()
        template = self.company_id.sf_onboarding_default_template
        if not template:
            template = self.env['sf.onboarding.template'].search([
                ('program_type', '=', 'onboarding'),
                ('company_id', 'in', [False, self.company_id.id]),
            ], limit=1)
        if not template:
            return
        existing = self.env['sf.onboarding.program'].search([
            ('employee_id', '=', self.id),
            ('program_type', '=', 'onboarding'),
            ('state', 'in', ('draft', 'in_progress')),
        ])
        if existing:
            return
        program = self.env['sf.onboarding.program'].create({
            'employee_id': self.id,
            'program_type': 'onboarding',
            'template_id': template.id,
            'key_date': fields.Date.today(),
        })
        program._generate_tasks()
        program.action_start()