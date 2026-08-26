# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HseInspectionChecklist(models.Model):
    _name = 'sf.hse.inspection.checklist'
    _description = 'HSE Inspection Checklist'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    category = fields.Selection([
        ('safety', 'Safety'),
        ('hygiene', 'Hygiene'),
        ('environment', 'Environment'),
        ('fire', 'Fire'),
    ], string='Category', default='safety')
    item_ids = fields.One2many('sf.hse.inspection.checklist.item',
                               'checklist_id', string='Items')


class HseInspectionChecklistItem(models.Model):
    _name = 'sf.hse.inspection.checklist.item'
    _description = 'HSE Inspection Checklist Item'
    _order = 'sequence'

    checklist_id = fields.Many2one('sf.hse.inspection.checklist',
                                   string='Checklist',
                                   ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Question', required=True)
    expected_answer = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A'),
    ], string='Expected', default='yes')


class HseInspection(models.Model):
    _name = 'sf.hse.inspection'
    _description = 'HSE Inspection'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'inspection_date desc'

    name = fields.Char(string='Number', required=True,
                       default=lambda self: _('New'))
    inspection_date = fields.Date(string='Inspection Date',
                                  default=fields.Date.context_today,
                                  required=True)
    checklist_id = fields.Many2one('sf.hse.inspection.checklist',
                                   string='Checklist')
    location = fields.Char(string='Location')
    inspector_id = fields.Many2one('hr.employee', string='Inspector')
    items = fields.One2many('sf.hse.inspection.item', 'inspection_id',
                            string='Inspection Items')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    findings = fields.Text(string='Findings')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.onchange('checklist_id')
    def _onchange_checklist_id(self):
        if self.checklist_id:
            items = []
            for item in self.checklist_id.item_ids:
                items.append((0, 0, {
                    'question': item.name,
                    'result': 'na',
                }))
            self.items = items

    def action_do(self):
        for inspection in self:
            if inspection.state != 'draft':
                raise UserError(_('Only draft inspections can be done.'))
            inspection.state = 'done'
            inspection.message_post(body=_('Inspection completed.'))

    def action_close(self):
        for inspection in self:
            if inspection.state != 'done':
                raise UserError(_('Only done inspections can be closed.'))
            inspection.state = 'closed'
            inspection.message_post(body=_('Inspection closed.'))


class HseInspectionItem(models.Model):
    _name = 'sf.hse.inspection.item'
    _description = 'HSE Inspection Result Item'
    _order = 'sequence'

    inspection_id = fields.Many2one('sf.hse.inspection',
                                    string='Inspection',
                                    ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence')
    question = fields.Char(string='Question', required=True)
    result = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'N/A'),
    ], string='Result', default='na')
    observation = fields.Text(string='Observation')
    is_nonconformity = fields.Boolean(string='Non-conformity',
                                      compute='_compute_nonconformity',
                                      store=True)

    @api.depends('result')
    def _compute_nonconformity(self):
        for item in self:
            item.is_nonconformity = item.result == 'no'