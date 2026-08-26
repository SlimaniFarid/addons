# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SeniorLivingActivityMixin(models.AbstractModel):
    _name = 'sf.senior.living.activity.mixin'
    _description = 'Senior Living Activity Mixin'

    activity_ids = fields.One2many(
        'sf.senior.living.activity', 'resident_id',
        string='Activities')
    activity_count = fields.Integer(
        string='Activity Count', compute='_compute_activity_count')

    @api.depends('activity_ids')
    def _compute_activity_count(self):
        for record in self:
            record.activity_count = len(record.activity_ids)

    def action_view_activities(self):
        self.ensure_one()
        return {
            'name': _('Activities'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.senior.living.activity',
            'view_mode': 'list,form',
            'domain': [('resident_id', '=', self.id)],
            'context': {'default_resident_id': self.id},
        }