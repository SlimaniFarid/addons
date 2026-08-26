# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfRentalInspection(models.Model):
    _name = 'sf.rental.inspection'
    _description = 'Rental Inspection'
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    contract_id = fields.Many2one('sf.rental.contract', string='Contract', required=True, ondelete='cascade')
    line_id = fields.Many2one('sf.rental.contract.line', string='Line', ondelete='cascade')
    direction = fields.Selection([
        ('out', 'Out'),
        ('in', 'In'),
    ], string='Direction', required=True, default='out')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('worn', 'Worn'),
        ('damaged', 'Damaged'),
        ('broken', 'Broken'),
    ], string='Condition')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', copy=False)
    damage_ids = fields.One2many('sf.rental.damage', 'inspection_id', string='Damages')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.inspection')
            if vals.get('contract_id') and not vals.get('company_id'):
                contract = self.env['sf.rental.contract'].browse(vals['contract_id'])
                vals['company_id'] = contract.company_id.id
            if vals.get('state', 'draft') != 'draft':
                raise UserError(_('Inspections can only be created in draft.'))
        return super().create(vals_list)

    def action_done(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft inspections can be completed.'))
        if self.direction == 'out' and not self.condition:
            self.condition = 'good'
        if self.direction == 'in' and self.condition in ('damaged', 'broken') and not self.damage_ids:
            raise UserError(_('A damaged or broken return requires at least one damage record.'))
        self.date = fields.Datetime.now()
        self.state = 'done'