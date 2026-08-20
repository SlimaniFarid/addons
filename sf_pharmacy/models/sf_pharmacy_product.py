# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PharmacyProduct(models.Model):
    _name = 'sf.pharmacy.product'
    _description = 'Produit pharmaceutique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom', readonly=True)
    generic_name = fields.Char(string='Nom générique')
    dosage = fields.Char(string='Dosage')
    form = fields.Selection([
        ('comprime', 'Comprimé'),
        ('gelule', 'Gélule'),
        ('sirop', 'Sirop'),
        ('pommade', 'Pommade'),
        ('injectable', 'Injectable'),
        ('collyre', 'Collyre'),
        ('autre', 'Autre'),
    ], string='Forme')
    atc_code = fields.Char(string='Code ATC')
    price_unit = fields.Monetary(string='Prix unitaire', currency_field='currency_id')
    cost = fields.Monetary(string='Coût', currency_field='currency_id')
    safety_stock = fields.Float(string='Stock de sécurité')
    active = fields.Boolean(string='Actif', default=True)
    responsible_id = fields.Many2one('res.users', string='Responsable')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Société', default=lambda self: self.env.company, ondelete='cascade')
    batch_ids = fields.One2many('sf.pharmacy.batch', 'product_id', string='Lots')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.product')
        return super(PharmacyProduct, self).create(vals)

    def action_open_batches(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lots',
            'res_model': 'sf.pharmacy.batch',
            'view_mode': 'tree,form',
            'domain': [('product_id', '=', self.id)],
        }
