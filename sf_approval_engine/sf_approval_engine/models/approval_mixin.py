# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ApprovalMixin(models.AbstractModel):
    """Abstract mixin to add approval to any document model."""

    _name = 'sf.approval.mixin'
    _description = 'Approval Mixin'

    approval_ids = fields.One2many(
        'sf.approval.request',
        'res_id',
        string='Approvals',
        domain=lambda self: [('res_model', '=', self._name)],
        auto_join=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._maybe_create_approval()
        return records

    def _maybe_create_approval(self):
        for record in self:
            if not self.env.context.get('sf_skip_approval'):
                template = self.env['sf.approval.template'].search([
                    ('model_id.model', '=', record._name),
                    ('active', '=', True),
                ], order='sequence asc, id asc', limit=1)
                if template:
                    self.env['sf.approval.request'].create({
                        'template_id': template.id,
                        'res_model': record._name,
                        'res_id': record.id,
                        'document_name': record.display_name,
                        'amount': record._get_approval_amount(),
                        'state': 'draft',
                    })

    def _get_approval_amount(self):
        for field in ('amount_total', 'total_amount', 'amount'):
            if field in self._fields:
                return self[field]
        return 0.0