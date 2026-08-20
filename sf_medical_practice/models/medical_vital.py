# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMedicalVital(models.Model):
    _name = 'sf.medical.vital'
    _description = 'Vital Signs'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True, copy=False)
    patient_id = fields.Many2one('sf.medical.patient', string='Patient',
                                 required=True, ondelete='restrict',
                                 index=True)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    weight = fields.Float(string='Weight (kg)')
    height = fields.Float(string='Height (cm)')
    bmi = fields.Float(string='BMI', compute='_compute_bmi', store=True)
    blood_pressure = fields.Char(string='Blood pressure')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        for vital in self:
            if vital.height and vital.height > 0:
                vital.bmi = vital.weight / ((vital.height / 100) ** 2)
            else:
                vital.bmi = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.medical.vital')
        return super().create(vals_list)

    def action_done(self):
        for vital in self:
            if vital.state != 'draft':
                raise UserError(_('Only draft vital signs can be '
                                  'validated.'))
            vital.state = 'done'