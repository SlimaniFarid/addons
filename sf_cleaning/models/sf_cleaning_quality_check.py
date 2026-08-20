# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCleaningQualityCheck(models.Model):
    _name = 'sf.cleaning.quality_check'
    _description = 'Cleaning Quality Check'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)
    schedule_line_id = fields.Many2one(
        'sf.cleaning.schedule.line', string='Intervention',
        ondelete='cascade', required=True, index=True)
    checker_id = fields.Many2one(
        'res.users', string='Checker',
        default=lambda self: self.env.user)
    check_date = fields.Date(
        string='Check date', default=fields.Date.context_today)
    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Rating')
    redo_required = fields.Boolean(string='Redo required')
    comments = fields.Text(string='Comments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.cleaning.quality_check')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_cleaning.group_sf_cleaning_manager'):
            raise UserError(_('Only managers can perform this action.'))

    def unlink(self):
        self._check_manager()
        return super().unlink()

    def action_validate(self):
        for check in self:
            if check.state != 'draft':
                raise UserError(_('Only draft quality checks can be '
                                  'validated.'))
            if not check.rating:
                raise UserError(_('A rating is required to validate the '
                                  'quality check.'))
        self.state = 'done'