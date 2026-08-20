# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class PharmacyBatchMovement(models.Model):
    _name = 'sf.pharmacy.batch_movement'
    _description = 'Mouvement de lot'
    _order = 'move_date desc, id desc'

    name = fields.Char(string='Mouvement', readonly=True)
    batch_id = fields.Many2one('sf.pharmacy.batch', string='Lot', required=True, ondelete='cascade', index=True)
    movement_type = fields.Selection([
        ('in', 'Entrée'),
        ('out', 'Sortie'),
        ('withdrawal', 'Retrait'),
        ('adjustment', 'Ajustement'),
        ('recall', 'Rappel'),
    ], string='Type de mouvement', required=True)
    qty = fields.Float(string='Quantité', required=True)
    unit_price = fields.Monetary(string='Prix unitaire', currency_field='currency_id')
    move_date = fields.Datetime(string='Date', default=fields.Datetime.now, index=True)
    reference = fields.Char(string='Référence')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Société', default=lambda self: self.env.company, ondelete='cascade')

    @api.model
    def create(self, vals):
        batch = self.env['sf.pharmacy.batch'].browse(vals.get('batch_id'))
        mtype = vals.get('movement_type')
        qty = vals.get('qty', 0.0)
        if mtype in ('withdrawal', 'recall', 'adjustment'):
            self._check_manager()
        if mtype == 'in':
            batch.write({'qty_received': batch.qty_received + qty})
        elif mtype == 'out':
            if batch.status in ('expired', 'withdrawn', 'recalled'):
                raise UserError(_('Délivrance interdite sur un lot périmé, retiré ou rappelé.'))
            if qty > batch.qty_available:
                raise UserError(_('Quantité insuffisante en stock pour le lot.'))
        elif mtype == 'withdrawal':
            if qty > batch.qty_available:
                raise UserError(_('Quantité insuffisante en stock pour le lot.'))
        elif mtype == 'recall':
            if qty > batch.qty_available:
                raise UserError(_('Quantité insuffisante en stock pour le lot.'))
        elif mtype == 'adjustment':
            new_received = batch.qty_received + qty
            new_available = new_received - batch.qty_dispensed - batch.qty_reserved - batch.qty_withdrawn
            if new_available < 0:
                raise UserError(_('Stock négatif impossible.'))
            batch.write({'qty_received': new_received})
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.batch_movement')
        return super(PharmacyBatchMovement, self).create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_pharmacy.group_sf_pharmacy_manager'):
            raise AccessError(_('Action réservée au groupe manager.'))
