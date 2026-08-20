# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AgriTreatment(models.Model):
    _name = 'sf.agri.treatment'
    _description = 'Agricultural Treatment'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Treatment', required=True, index=True)
    culture_id = fields.Many2one('sf.agri.culture', string='Culture',
                                 required=True, ondelete='cascade',
                                 index=True)
    treatment_type = fields.Selection([
        ('insecticide', 'Insecticide'),
        ('fungicide', 'Fungicide'),
        ('herbicide', 'Herbicide'),
        ('fertilizer', 'Fertilizer'),
        ('other', 'Other'),
    ], string='Type', default='other', required=True)
    product = fields.Char(string='Product')
    active_ingredient = fields.Char(string='Active ingredient')
    quantity = fields.Float(string='Quantity', default=0.0)
    unit = fields.Selection([
        ('kg', 'kg'),
        ('l', 'l'),
        ('g', 'g'),
        ('m', 'm'),
    ], string='Unit', default='kg')
    treatment_date = fields.Date(string='Treatment date')
    withdrawal_days = fields.Integer(string='Withdrawal period (days)',
                                     default=0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('applied', 'Applied'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.agri.treatment')
        return super().create(vals)

    def action_plan(self):
        for treatment in self:
            if treatment.state != 'draft':
                raise UserError(_('Only draft treatments can be planned.'))
            treatment.state = 'planned'

    def action_apply(self):
        for treatment in self:
            if treatment.state != 'planned':
                raise UserError(_('Only planned treatments can be applied.'))
            treatment.state = 'applied'

    def action_done(self):
        for treatment in self:
            if treatment.state != 'applied':
                raise UserError(_('Only applied treatments can be done.'))
            treatment.state = 'done'

    def _check_agri_alerts(self):
        today = fields.Date.today()
        activity_todo = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            treatments = self.with_company(company).search([
                ('state', 'in', ['planned', 'applied']),
                ('withdrawal_days', '>', 0),
                ('treatment_date', '!=', False),
                ('company_id', '=', company.id),
            ])
            for treatment in treatments:
                culture = treatment.culture_id
                alert_date = treatment.treatment_date + timedelta(
                    days=treatment.withdrawal_days)
                harvest_date = culture.harvest_date if culture else False
                if not harvest_date:
                    continue
                if harvest_date >= alert_date:
                    continue
                existing = treatment.activity_ids.filtered(
                    lambda a: a.activity_type_id == activity_todo
                    and a.state != 'done')
                if existing:
                    continue
                treatment.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Withdrawal period not respected: %s')
                    % (culture.name if culture else treatment.name),
                    user_id=self.env.user.id)