from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RMARequest(models.Model):
    _name = 'rma.request'
    _description = 'RMA Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='RMA Number', required=True, copy=False, default='New')
    channel = fields.Selection([
        ('ecommerce', 'eCommerce'),
        ('pos', 'POS'),
        ('b2b', 'B2B'),
        ('marketplace', 'Marketplace'),
        ('manual', 'Manual'),
    ], string='Channel', required=True, default='manual')

    sale_order_id = fields.Many2one('sale.order', string='Original Order', ondelete='set null')
    pos_order_id = fields.Many2one('pos.order', string='Original POS Order', ondelete='set null')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('received', 'Received'),
        ('inspected', 'Inspected'),
        ('dispositioned', 'Dispositioned'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    reason = fields.Selection([
        ('defective', 'Defective'),
        ('wrong_item', 'Wrong Item Shipped'),
        ('damaged', 'Damaged in Transit'),
        ('not_as_described', 'Not as Described'),
        ('changed_mind', 'Changed Mind'),
        ('size_fit', 'Size/Fit Issue'),
        ('quality', 'Quality Issue'),
        ('other', 'Other'),
    ], string='Return Reason', required=True)

    reason_description = fields.Text(string='Details')
    requested_date = fields.Date(string='Requested Date', default=fields.Date.today)
    approved_date = fields.Date(string='Approved Date')
    received_date = fields.Date(string='Received Date')

    line_ids = fields.One2many('rma.line', 'request_id', string='Return Lines')
    total_qty = fields.Float(string='Total Quantity', compute='_compute_totals')
    total_refund = fields.Monetary(string='Total Refund', compute='_compute_totals', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)

    # RMA Process
    carrier_label_id = fields.Many2one('rma.carrier.label', string='Return Label')
    inspection_id = fields.Many2one('rma.inspection', string='Inspection')
    disposition_id = fields.Many2one('rma.disposition', string='Disposition')

    # Auto-approval
    auto_approved = fields.Boolean(string='Auto-Approved', readonly=True)
    rule_id = fields.Many2one('rma.rule', string='Applied Rule', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('rma.request') or 'RMA-%s' % self.env['ir.sequence'].next_by_code('rma.request')
        return super().create(vals_list)

    @api.depends('line_ids.quantity', 'line_ids.refund_amount')
    def _compute_totals(self):
        for rma in self:
            rma.total_qty = sum(l.quantity for l in rma.line_ids)
            rma.total_refund = sum(l.refund_amount for l in rma.line_ids)

    def action_submit(self):
        self.write({'state': 'submitted'})
        self._check_auto_approval()

    def _check_auto_approval(self):
        for rma in self:
            rule = self.env['rma.rule']._find_matching_rule(rma)
            if rule and rule.auto_approve:
                rma.write({'state': 'approved', 'auto_approved': True, 'rule_id': rule.id, 'approved_date': fields.Date.today()})

    def action_approve(self):
        self.write({'state': 'approved', 'approved_date': fields.Date.today()})
        # Generate return label if configured
        if self.rule_id and self.rule_id.generate_label:
            self.action_generate_label()

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_generate_label(self):
        # Create carrier label
        label = self.env['rma.carrier.label'].create({
            'rma_id': self.id,
            'carrier_id': self.rule_id.carrier_id.id if self.rule_id else False,
        })
        self.carrier_label_id = label.id

    def action_receive(self):
        self.write({'state': 'received', 'received_date': fields.Date.today()})

    def action_inspect(self):
        inspection = self.env['rma.inspection'].create({
            'rma_id': self.id,
            'inspector_id': self.env.user.id,
        })
        self.write({'state': 'inspected', 'inspection_id': inspection.id})

    def action_close(self):
        self.write({'state': 'closed'})


class RMALine(models.Model):
    _name = 'rma.line'
    _description = 'RMA Line'

    request_id = fields.Many2one('rma.request', string='RMA Request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    original_qty = fields.Float(string='Original Quantity')
    quantity = fields.Float(string='Return Quantity', required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='UoM', related='product_id.uom_id', readonly=True)

    unit_price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    refund_amount = fields.Monetary(string='Refund Amount', currency_field='currency_id', compute='_compute_refund')
    currency_id = fields.Many2one(related='request_id.currency_id', store=True)

    condition = fields.Selection([
        ('new', 'New/Unopened'),
        ('like_new', 'Like New'),
        ('used', 'Used'),
        ('damaged', 'Damaged'),
    ], string='Condition')

    @api.depends('quantity', 'unit_price')
    def _compute_refund(self):
        for line in self:
            line.refund_amount = line.quantity * line.unit_price