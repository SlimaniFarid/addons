# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfBatchRecordMaterial(models.Model):
    _name = 'sf.batch.record.material'
    _description = 'Batch Record Material'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.batch.record.activity.mixin']
    _order = 'id asc'

    batch_record_id = fields.Many2one('sf.batch.record', string='Batch Record',
                                      required=True, ondelete='cascade', index=True)
    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 ondelete='restrict')
    lot_id = fields.Many2one('stock.lot', string='Lot', ondelete='set null')
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    uom_name = fields.Char(string='Unit of Measure')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_quantity_positive',
         'CHECK (quantity > 0)',
         'The material quantity must be greater than zero.'),
    ]

    @api.constrains('quantity')
    def _check_quantity(self):
        for material in self:
            if material.quantity <= 0:
                raise ValidationError(_('The material quantity must be greater than zero.'))

    def _check_editable(self):
        self.ensure_one()
        if self.batch_record_id.state in ('released', 'rejected', 'cancelled'):
            raise UserError(_('A finished batch record cannot be modified.'))

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('batch_record_id'):
                parent = self.env['sf.batch.record'].browse(vals['batch_record_id'])
                if parent.state in ('released', 'rejected', 'cancelled'):
                    raise UserError(_('A finished batch record cannot be modified.'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._check_editable()
        return super().write(vals)

    def unlink(self):
        for record in self:
            record._check_editable()
        return super().unlink()