# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class VendorContractRenewWizard(models.TransientModel):
    _name = 'sf.vendor.contract.renew.wizard'
    _description = 'Renew Contract Wizard'

    contract_id = fields.Many2one('sf.vendor.contract',
                                  string='Contract', required=True,
                                  readonly=True)
    new_date_start = fields.Date(string='New Start Date',
                                 required=True,
                                 default=fields.Date.today)
    new_date_end = fields.Date(string='New End Date', required=True)
    new_amount = fields.Monetary(string='New Total Amount',
                                 currency_field='currency_id',
                                 default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='contract_id.currency_id')
    version = fields.Char(string='Version', required=True,
                          default='v2')

    def action_renew(self):
        self.ensure_one()
        contract = self.contract_id
        if contract.state not in ('active', 'expiring', 'expired'):
            raise UserError(
                _('Only active, expiring or expired contracts '
                  'can be renewed.'))
        if not self.new_date_end:
            raise UserError(
                _('A new end date is required to renew a contract.'))
        if self.new_date_end < self.new_date_start:
            raise UserError(
                _('The new end date cannot be before the new '
                  'start date.'))
        contract._create_version(contract.version_ids and
                                 'v%d' % (len(contract.version_ids) + 1)
                                 or 'v1')
        old_state = contract.state
        contract.write({
            'date_start': self.new_date_start,
            'date_end': self.new_date_end,
            'amount_total': self.new_amount,
            'state': 'renewed',
        })
        contract.message_post(body=_(
            'Contract renewed from version %s (previous status: %s).')
            % (self.version, old_state))
        new_contract = contract.copy({
            'state': 'active',
            'date_start': self.new_date_start,
            'date_end': self.new_date_end,
            'amount_total': self.new_amount,
            'clause_ids': [(5, 0, 0)],
            'line_ids': [(5, 0, 0)],
            'version_ids': [(5, 0, 0)],
            'name': '%s (%s)' % (contract.name, self.version),
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.vendor.contract',
            'res_id': new_contract.id,
            'view_mode': 'form',
        }


class VendorContractCancelWizard(models.TransientModel):
    _name = 'sf.vendor.contract.cancel.wizard'
    _description = 'Cancel Contract Wizard'

    contract_id = fields.Many2one('sf.vendor.contract',
                                  string='Contract', required=True,
                                  readonly=True)
    reason = fields.Text(string='Reason', required=True)

    def action_cancel(self):
        self.ensure_one()
        contract = self.contract_id
        if contract.state == 'expired':
            raise UserError(
                _('An expired contract cannot be cancelled.'))
        contract.write({'state': 'cancelled'})
        contract.message_post(body=_('Contract cancelled: %s')
                              % self.reason)
        return {'type': 'ir.actions.act_window_close'}