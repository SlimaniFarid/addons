# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class SchoolPaymentWizard(models.TransientModel):
    _name = 'sf.school.payment.wizard'
    _description = 'Record Tuition Payment'

    tuition_id = fields.Many2one('sf.school.tuition', string='Tuition',
                                 required=True, readonly=True)
    amount = fields.Float(string='Payment amount', required=True)

    def action_record_payment(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_school_management.group_school_manager'):
            raise UserError(_('Only school managers can record payments.'))
        if self.amount <= 0:
            raise UserError(_('The payment amount must be positive.'))
        tuition = self.tuition_id
        tuition.write({'paid_amount': tuition.paid_amount + self.amount})
        return {'type': 'ir.actions.act_window_close'}