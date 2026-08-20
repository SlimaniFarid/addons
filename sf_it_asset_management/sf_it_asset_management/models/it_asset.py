# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ItAsset(models.Model):
    _name = 'sf.it.asset'
    _description = 'IT Asset'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    asset_tag = fields.Char(string='Asset Tag', index=True)
    category_id = fields.Many2one('sf.it.asset.category',
                                  string='Category', required=True)
    partner_vendor_id = fields.Many2one('res.partner',
                                        string='Vendor')
    purchase_date = fields.Date(string='Purchase Date')
    warranty_expiration = fields.Date(string='Warranty Expiration')
    serial_number = fields.Char(string='Serial Number')
    purchase_value = fields.Monetary(string='Purchase Value',
                                     currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_stock', 'In Stock'),
        ('assigned', 'Assigned'),
        ('maintenance', 'In Maintenance'),
        ('retired', 'Retired'),
        ('lost', 'Lost'),
    ], string='Status', default='draft', tracking=True)
    assignee_id = fields.Many2one('hr.employee', string='Assigned To',
                                  compute='_compute_assignment', store=True)
    assignment_date = fields.Date(string='Assigned On',
                                  compute='_compute_assignment', store=True)
    active_assignment_id = fields.Many2one('sf.it.assignment',
                                           string='Active Assignment',
                                           compute='_compute_assignment',
                                           store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

    @api.depends('active_assignment_id', 'active_assignment_id.employee_id',
                 'active_assignment_id.date_from')
    def _compute_assignment(self):
        for asset in self:
            assignment = asset.active_assignment_id
            asset.assignee_id = assignment.employee_id
            asset.assignment_date = assignment.date_from

    def _get_active_assignment(self):
        self.ensure_one()
        return self.env['sf.it.assignment'].search([
            ('asset_id', '=', self.id),
            ('state', '=', 'active'),
        ], limit=1)

    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        for asset in self:
            if asset.purchase_value and asset.purchase_value < 0:
                raise UserError(
                    _('The purchase value cannot be negative.'))

    @api.constrains('purchase_date', 'warranty_expiration')
    def _check_warranty(self):
        for asset in self:
            if (asset.purchase_date and asset.warranty_expiration
                    and asset.warranty_expiration < asset.purchase_date):
                raise UserError(
                    _('The warranty expiration must be after the '
                      'purchase date.'))

    def action_assign(self):
        view = self.env.ref('sf_it_asset_management.it_asset_assignment_wizard_form')
        return {
            'name': _('Assign Asset'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.it.assignment.wizard',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'context': {'default_asset_id': self.id},
        }

    def action_unassign(self):
        for asset in self:
            assignment = asset._get_active_assignment()
            if not assignment:
                raise UserError(_('This asset has no active assignment.'))
            assignment.action_close()
        return True

    def action_to_maintenance(self):
        for asset in self:
            if asset.state != 'assigned':
                raise UserError(
                    _('Only assigned assets can be sent to maintenance. '
                      'Unassign the asset first.'))
            asset.state = 'maintenance'

    def action_from_maintenance(self):
        for asset in self:
            if asset.state != 'maintenance':
                raise UserError(
                    _('Only assets in maintenance can be returned.'))
            asset.state = 'in_stock'

    def action_retire(self):
        for asset in self:
            if asset.state == 'assigned':
                raise UserError(
                    _('An assigned asset cannot be retired. '
                      'Unassign it first.'))
            asset.state = 'retired'

    def action_report_lost(self):
        for asset in self:
            if asset.state == 'assigned':
                assignment = asset._get_active_assignment()
                if assignment:
                    assignment.write({'state': 'closed', 'date_to':
                                      fields.Date.today(),
                                      'notes': _('Asset reported lost.')})
            asset.state = 'lost'

    def action_to_stock(self):
        for asset in self:
            if asset.state == 'draft':
                asset.state = 'in_stock'

    def unlink(self):
        for asset in self:
            if asset.state == 'assigned':
                raise UserError(
                    _('An assigned asset cannot be deleted. '
                      'Unassign it first.'))
        return super().unlink()