# -*- coding: utf-8 -*-
from odoo import models


class SfPolicyActivityMixin(models.AbstractModel):
    _name = 'sf.policy.activity.mixin'
    _description = 'Policy Activity Mixin'

    def _sf_check_todo(self, todo_type, subject, note=None, user_id=None):
        self.ensure_one()
        existing = self.activity_ids.filtered(
            lambda a: a.activity_type_id == todo_type
            and a.summary == subject
            and not a.done
        )
        if existing:
            return existing[0]
        return self.activity_schedule(
            todo_type,
            summary=subject,
            note=note,
            user_id=user_id or self.env.user.id,
        )