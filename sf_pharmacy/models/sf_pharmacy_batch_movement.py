# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class PharmacyBatchMovement(models.Model):
    _name = 'sf.pharmacy.batch_movement'
    _description = 'Batch movement'
    _order = 'move_date desc, id desc'

    name = fields.Char(string='Movement', readonly=True)
    batch_id = fields.Many2one('sf.pharmacy.batch', string='Batch', required=True, ondelete='cascade', index=True)
    movement_type = fields.Selection([
        ('in', 'In'),
        ('out', 'Out'),
        ('withdrawal', 'Withdrawal'),
        ('adjustment', 'Adjustment'),
        ('recall', 'Recall'),
    ], string='Movement type', required=True)
    qty = fields.Float(string='Quantity', required=True)
    unit_price = fields.Monetary(string='Unit price', currency_field='currency_id')
    move_date = fields.Datetime(string='Date', default=fields.Datetime.now, index=True)
    reference = fields.Char(string='Reference')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, ondelete='cascade')

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
                raise UserError(_('Dispensation forbidden on an expired, withdrawn or recalled batch.'))
            if qty > batch.qty_available:
                raise UserError(_('Insufficient stock quantity for the batch.'))
        elif mtype == 'withdrawal':
            if qty > batch.qty_available:
                raise UserError(_('Insufficient stock quantity for the batch.'))
        elif mtype == 'recall':
            if qty > batch.qty_available:
                raise UserError(_('Insufficient stock quantity for the batch.'))
        elif mtype == 'adjustment':
            new_received = batch.qty_received + qty
            new_available = new_received - batch.qty_dispensed - batch.qty_reserved - batch.qty_withdrawn
            if new_available < 0:
                raise UserError(_('Negative stock is not allowed.'))
            batch.write({'qty_received': new_received})
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.batch_movement')
        return super(PharmacyBatchMovement, self).create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_pharmacy.group_sf_pharmacy_manager'):
            raise AccessError(_('Action reserved for the manager group.'))
