# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PharmacyProduct(models.Model):
    _name = 'sf.pharmacy.product'
    _description = 'Pharmaceutical product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', readonly=True)
    generic_name = fields.Char(string='Generic name')
    dosage = fields.Char(string='Dosage')
    form = fields.Selection([
        ('comprime', 'Tablet'),
        ('gelule', 'Capsule'),
        ('sirop', 'Syrup'),
        ('pommade', 'Ointment'),
        ('injectable', 'Injectable'),
        ('collyre', 'Eye drops'),
        ('autre', 'Other'),
    ], string='Form')
    atc_code = fields.Char(string='ATC Code')
    price_unit = fields.Monetary(string='Unit price', currency_field='currency_id')
    cost = fields.Monetary(string='Cost', currency_field='currency_id')
    safety_stock = fields.Float(string='Safety stock')
    active = fields.Boolean(string='Active', default=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, ondelete='cascade')
    batch_ids = fields.One2many('sf.pharmacy.batch', 'product_id', string='Batches')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.product')
        return super(PharmacyProduct, self).create(vals)

    def action_open_batches(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Batches',
            'res_model': 'sf.pharmacy.batch',
            'view_mode': 'tree,form',
            'domain': [('product_id', '=', self.id)],
        }
