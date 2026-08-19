# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class ItAssetAssignmentWizard(models.TransientModel):
    _name = 'sf.it.assignment.wizard'
    _description = 'IT Asset Assignment Wizard'

    asset_id = fields.Many2one('sf.it.asset', string='Asset',
                               required=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    date_from = fields.Date(string='From', required=True,
                            default=fields.Date.today)
    notes = fields.Text(string='Notes')

    def action_assign(self):
        self.ensure_one()
        if self.asset_id.state != 'in_stock':
            raise UserError(
                _('Only assets in stock can be assigned.'))
        self.env['sf.it.assignment'].create({
            'asset_id': self.asset_id.id,
            'employee_id': self.employee_id.id,
            'date_from': self.date_from,
            'notes': self.notes,
        })
        self.asset_id.state = 'assigned'
        return {'type': 'ir.actions.act_window_close'}


class ItLicenseRenewWizard(models.TransientModel):
    _name = 'sf.it.license.renew.wizard'
    _description = 'IT License Renewal Wizard'

    license_id = fields.Many2one('sf.it.license', string='License',
                                 required=True, readonly=True)
    new_expiration = fields.Date(string='New Expiration Date',
                                 required=True)

    def action_renew(self):
        self.ensure_one()
        license = self.license_id
        if license.state == 'draft':
            raise UserError(_('The license must be active to be renewed.'))
        license.write({
            'expiration_date': self.new_expiration,
            'state': 'renewed',
        })
        license.message_post(body=_('License renewed until %s.')
                             % self.new_expiration)
        new_license = license.copy({
            'state': 'active',
            'expiration_date': self.new_expiration,
            'name': '%s (renewed)' % license.name,
            'assignments': [(5, 0, 0)],
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.it.license',
            'res_id': new_license.id,
            'view_mode': 'form',
        }