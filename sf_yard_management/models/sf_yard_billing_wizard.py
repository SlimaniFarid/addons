# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardBillingWizard(models.TransientModel):
    _name = 'sf.yard.billing.wizard'
    _description = 'Bill Detention to Carrier'

    carrier_id = fields.Many2one('res.partner', string='Carrier',
                                 required=True,
                                 domain=[('is_company', '=', True)])
    date_from = fields.Date(string='From', required=True,
                            default=lambda self: fields.Date.today()
                            .replace(day=1))
    date_to = fields.Date(string='To', required=True,
                          default=fields.Date.today)

    def action_bill(self):
        self.ensure_one()
        Detention = self.env['sf.yard.detention']
        detentions = Detention.search([
            ('carrier_id', '=', self.carrier_id.id),
            ('status', '=', 'chargeable'),
            ('company_id', '=', self.env.company.id),
        ])
        detentions = detentions.filtered(
            lambda d: d.arrived_at and d.arrived_at.date() >= self.date_from
            and d.arrived_at.date() <= self.date_to)
        if not detentions:
            raise UserError(_('No chargeable detention found for this '
                              'carrier in the selected period.'))
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.env.company.id),
            ('type', '=', 'purchase'),
        ], limit=1)
        if not journal:
            raise UserError(_('No purchase journal found.'))
        account = self.env['account.account'].search([
            ('account_type', '=', 'expense'),
            ('company_id', '=', self.env.company.id),
        ], limit=1)
        lines = [(0, 0, {
            'name': _('Detention %s — %.1fh billable')
            % (d.trailer_id.name, d.billable_hours),
            'quantity': 1,
            'price_unit': d.total_amount,
            'account_id': account.id if account else False,
        }) for d in detentions]
        move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.carrier_id.id,
            'invoice_date': fields.Date.context_today(self),
            'journal_id': journal.id,
            'invoice_line_ids': lines,
        })
        move.action_post()
        detentions.write({
            'status': 'invoiced',
            'invoice_id': move.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Detention Invoice'),
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'list,form',
        }
