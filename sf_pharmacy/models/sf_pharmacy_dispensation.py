# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PharmacyDispensation(models.Model):
    _name = 'sf.pharmacy.dispensation'
    _description = 'Délivrance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'dispensed_at desc, id desc'

    name = fields.Char(string='Délivrance', readonly=True)
    prescription_id = fields.Many2one('sf.pharmacy.prescription', string='Ordonnance', required=True, ondelete='cascade')
    product_id = fields.Many2one('sf.pharmacy.product', string='Produit', required=True, ondelete='restrict', index=True)
    batch_id = fields.Many2one('sf.pharmacy.batch', string='Lot', required=True, ondelete='restrict', index=True)
    qty = fields.Float(string='Quantité', required=True)
    posology = fields.Text(string='Posologie')
    dispensed_by = fields.Many2one('res.users', string='Délivré par', readonly=True)
    dispensed_at = fields.Datetime(string='Délivré le', readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], string='Statut', default='draft')
    company_id = fields.Many2one('res.company', string='Société', default=lambda self: self.env.company, ondelete='cascade')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and not self.batch_id:
            company_id = self.company_id.id or self.env.company.id
            self.batch_id = self.env['sf.pharmacy.batch']._get_fifo_batch(self.product_id.id, company_id=company_id)

    @api.model
    def create(self, vals):
        if vals.get('product_id') and not vals.get('batch_id'):
            company_id = vals.get('company_id') or self.env.company.id
            batch = self.env['sf.pharmacy.batch']._get_fifo_batch(vals['product_id'], company_id=company_id)
            if batch:
                vals['batch_id'] = batch.id
        batch = self.env['sf.pharmacy.batch'].browse(vals.get('batch_id'))
        if batch:
            if batch.status in ('expired', 'withdrawn', 'recalled'):
                raise UserError(_('Délivrance interdite sur un lot périmé, retiré ou rappelé.'))
            if vals.get('qty', 0.0) > batch.qty_available:
                raise UserError(_('Quantité insuffisante en stock pour le lot.'))
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.dispensation')
        return super(PharmacyDispensation, self).create(vals)

    def write(self, vals):
        if vals.get('state') == 'done':
            vals.setdefault('dispensed_at', fields.Datetime.now())
            vals.setdefault('dispensed_by', self.env.user.id)
        return super(PharmacyDispensation, self).write(vals)

    def action_done(self):
        for line in self:
            if line.state == 'done':
                continue
            if line.state == 'cancelled':
                raise UserError(_('Une délivrance annulée ne peut être terminée.'))
            if line.batch_id.status in ('expired', 'withdrawn', 'recalled'):
                raise UserError(_('Délivrance interdite sur un lot périmé, retiré ou rappelé.'))
            if line.qty > line.batch_id.qty_available:
                raise UserError(_('Quantité insuffisante en stock pour le lot.'))
            self.env['sf.pharmacy.batch_movement'].create({
                'batch_id': line.batch_id.id,
                'movement_type': 'out',
                'qty': line.qty,
                'unit_price': line.product_id.price_unit,
                'reference': line.prescription_id.name,
                'company_id': line.company_id.id,
            })
            line.write({
                'state': 'done',
                'dispensed_at': fields.Datetime.now(),
                'dispensed_by': self.env.user.id,
            })
        return True

    def action_cancel(self):
        for line in self:
            if line.state == 'done':
                raise UserError(_('Une délivrance terminée ne peut être annulée.'))
            line.state = 'cancelled'
        return True
