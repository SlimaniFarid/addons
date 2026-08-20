# -*- coding: utf-8 -*-
from odoo import fields, models


class SfStoreCreditAdjustWizard(models.TransientModel):
    _name = 'sf.store.credit.adjust.wizard'
    _description = 'Store Credit Adjustment'

    credit_id = fields.Many2one('sf.store.credit', string='Credit', required=True)
    amount = fields.Monetary(string='Adjustment Amount', currency_field='currency_id',
                             required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='credit_id.currency_id', readonly=True)
    reason = fields.Char(string='Reason', required=True)

    def action_apply(self):
        self.ensure_one()
        self.credit_id.action_adjust(self.amount, self.reason)
        return {'type': 'ir.actions.act_window_close'}