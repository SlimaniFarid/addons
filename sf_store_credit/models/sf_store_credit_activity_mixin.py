# -*- coding: utf-8 -*-
from odoo import models


class SfStoreCreditActivityMixin(models.AbstractModel):
    _name = 'sf.store.credit.activity.mixin'
    _description = 'Store Credit Activity Mixin'

    def _sf_check_todo(self, todo_type, subject, note=None):
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
        )