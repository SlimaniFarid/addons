from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaRetailSale(models.Model):
    _name = 'sf.spa.retail.sale'
    _description = 'Retail Sale'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread']
    _order = 'name desc'
    _sequence_code = 'sf.spa.retail.sale'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client')
    booking_id = fields.Many2one('sf.spa.booking', string='Linked Treatment')
    therapist_id = fields.Many2one('sf.spa.therapist', string='Recommending Therapist')
    line_ids = fields.One2many('sf.spa.retail.sale.line', 'sale_id', string='Lines')
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('returned', 'Returned'),
    ], string='State', default='draft', tracking=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.depends('line_ids.price_subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('price_subtotal'))

    def action_done(self):
        for record in self:
            if record.state != 'draft':
                continue
            record.state = 'done'
            record._create_invoice()

    def action_return(self):
        for record in self:
            if record.state != 'done':
                continue
            record.state = 'returned'

    def _create_invoice(self):
        self.ensure_one()
        if not self.partner_id:
            return
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'discount': line.discount,
            }) for line in self.line_ids],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id


class SpaRetailSaleLine(models.Model):
    _name = 'sf.spa.retail.sale.line'
    _description = 'Retail Sale Line'
    _inherit = ['sf.spa.company.mixin']

    sale_id = fields.Many2one('sf.spa.retail.sale', string='Sale', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Monetary(string='Unit Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='sale_id.currency_id', readonly=True)
    discount = fields.Float(string='Discount (%)', default=0.0)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', store=True, currency_field='currency_id')
    commission_amount = fields.Monetary(string='Commission', compute='_compute_commission', store=True, currency_field='currency_id')

    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity * record.price_unit * (1 - record.discount / 100)

    @api.depends('price_subtotal', 'sale_id.therapist_id', 'sale_id.booking_id')
    def _compute_commission(self):
        for record in self:
            commission = 0.0
            if record.sale_id.therapist_id and record.sale_id.booking_id:
                commission = record.price_subtotal * record.sale_id.therapist_id.commission_on_retail / 100
            record.commission_amount = commission

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_('Quantity must be positive.'))

    @api.constrains('discount')
    def _check_discount(self):
        for record in self:
            if record.discount < 0 or record.discount > 100:
                raise ValidationError(_('Discount must be between 0 and 100.'))