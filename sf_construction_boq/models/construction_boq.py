from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ConstructionBoq(models.Model):
    _name = 'construction.boq'
    _description = 'Bill of Quantities'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    project_id = fields.Many2one('project.project', string='Project', ondelete='restrict', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Client', ondelete='restrict', tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False, tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    boq_line_ids = fields.One2many('construction.boq.line', 'boq_id', string='BOQ Lines')
    amount_total = fields.Monetary(string='Total', currency_field='currency_id',
                                   compute='_compute_amount_total', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('boq_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for boq in self:
            boq.amount_total = sum(boq.boq_line_ids.mapped('price_subtotal'))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.boq') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for boq in self:
            if not boq.boq_line_ids:
                raise UserError(_('Cannot confirm a BOQ without lines.'))
            boq.state = 'confirmed'

    def action_start(self):
        for boq in self:
            if boq.state != 'confirmed':
                raise UserError(_('Only a confirmed BOQ can be started.'))
            boq.state = 'in_progress'

    def action_done(self):
        for boq in self:
            boq.state = 'done'

    def action_cancel(self):
        for boq in self:
            if boq.state in ('done',):
                raise UserError(_('A done BOQ cannot be cancelled.'))
            boq.state = 'cancelled'


class ConstructionBoqLine(models.Model):
    _name = 'construction.boq.line'
    _description = 'BOQ Line'
    _order = 'boq_id, sequence, id'

    boq_id = fields.Many2one('construction.boq', string='BOQ', ondelete='cascade', required=True, index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    code = fields.Char(string='Code', copy=False)
    description = fields.Text(string='Description', required=True)
    category = fields.Selection([
        ('earthwork', 'Earthwork'),
        ('concrete', 'Concrete'),
        ('masonry', 'Masonry'),
        ('structure', 'Structure'),
        ('finishing', 'Finishing'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('hvac', 'HVAC'),
        ('roofing', 'Roofing'),
        ('other', 'Other'),
    ], string='Discipline', default='other')
    product_id = fields.Many2one('product.product', string='Product')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', default=lambda self: self.env.ref('uom.product_uom_unit', raise_if_not_found=False))
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    price_subtotal = fields.Monetary(string='Amount', currency_field='currency_id',
                                     compute='_compute_price_subtotal', store=True)
    currency_id = fields.Many2one('res.currency', related='boq_id.currency_id', readonly=True)

    @api.depends('quantity', 'unit_price')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.unit_price
