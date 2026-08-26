# -*- coding: utf-8 -*-
from odoo import fields, models


class SfUtilityActivityMixin(models.AbstractModel):
    _name = 'sf.utility.activity.mixin'
    _description = 'Utility Activity Mixin'

    activity_ids = fields.One2many('mail.activity', 'res_id', string='Activities', auto_join=True)

    def _sf_check_todo(self, activity_type, summary, note=None):
        self.ensure_one()
        existing = self.activity_ids.filtered(
            lambda a: a.activity_type_id.id == activity_type.id and a.summary == summary
        )
        if existing:
            return existing[:1]
        return self.activity_schedule(
            activity_type_id=activity_type.id,
            summary=summary,
            note=note or summary,
            user_id=self.env.user.id,
        )