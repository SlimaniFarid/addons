# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CpqConfiguration(models.Model):
    _name = 'sf.cpq.configuration'
    _description = 'CPQ Configuration'
    _rec_name = 'name'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', readonly=True)
    configurator_id = fields.Many2one('sf.cpq.configurator',
                                      string='Configurator',
                                      required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 related='configurator_id.product_id',
                                 store=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    option_ids = fields.Many2many('sf.cpq.option', string='Selected Options')
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    base_price = fields.Monetary(string='Base Price',
                                 compute='_compute_price', store=True)
    adjustments = fields.Monetary(string='Adjustments',
                                  compute='_compute_price', store=True)
    total_price = fields.Monetary(string='Total Price',
                                  compute='_compute_price', store=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('quoted', 'Quoted'),
    ], string='Status', default='draft')

    @api.depends('product_id', 'option_ids', 'quantity')
    def _compute_price(self):
        for cfg in self:
            base = cfg.product_id.list_price or 0.0
            adj = sum(cfg.option_ids.mapped('price_adjust') or [0.0])
            cfg.base_price = base
            cfg.adjustments = adj
            cfg.total_price = (base + adj) * cfg.quantity

    @api.model
    def create(self, vals):
        cfg = super().create(vals)
        cfg.name = self.env['ir.sequence'].next_by_code('sf.cpq.configuration') \
            or 'CPQ/'
        return cfg

    def action_quote(self):
        """Generate a quotation from this configuration."""
        self.ensure_one()
        Order = self.env['sale.order']
        if not self.partner_id:
            raise models.ValidationError(
                _('Please select a customer before generating a quote.'))
        order = Order.create({
            'partner_id': self.partner_id.id,
        })
        order.order_line.create({
            'order_id': order.id,
            'product_id': self.product_id.id,
            'name': self.name,
            'product_uom_qty': self.quantity,
            'price_unit': self.total_price / self.quantity if self.quantity else 0.0,
        })
        self.state = 'quoted'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id,
            'view_mode': 'form',
        }