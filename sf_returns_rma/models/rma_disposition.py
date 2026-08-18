from odoo import api, fields, models


class RMADisposition(models.Model):
    _name = 'rma.disposition'
    _description = 'RMA Disposition'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rma_id = fields.Many2one('rma.request', string='RMA Request', required=True, ondelete='cascade')
    inspection_id = fields.Many2one('rma.inspection', string='Inspection', ondelete='set null')

    action = fields.Selection([
        ('restock', 'Restock as New'),
        ('repack', 'Repack & Restock'),
        ('repair', 'Send to Repair'),
        ('refurbish', 'Refurbish'),
        ('scrap', 'Scrap'),
        ('return_vendor', 'Return to Vendor'),
        ('donate', 'Donate'),
    ], string='Action', required=True)

    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', tracking=True)

    # Restock
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    location_id = fields.Many2one('stock.location', string='Location')

    # Repair
    repair_order_id = fields.Many2one('repair.order', string='Repair Order')

    # Refurbish
    refurbish_cost = fields.Float(string='Refurbish Cost')
    new_sale_price = fields.Float(string='New Sale Price')

    # Scrap
    scrap_reason = fields.Char(string='Scrap Reason')

    # Return to Vendor
    vendor_rma_id = fields.Many2one('rma.vendor.rma', string='Vendor RMA')

    notes = fields.Text(string='Notes')

    def action_execute(self):
        for disp in self:
            if disp.action == 'restock':
                disp._action_restock()
            elif disp.action == 'repair':
                disp._action_repair()
            elif disp.action == 'scrap':
                disp._action_scrap()
            disp.write({'state': 'done'})

    def _action_restock(self):
        # Create stock move to put back in inventory
        for disp in self:
            for line in disp.rma_id.line_ids:
                self.env['stock.move'].create({
                    'name': f'RMA Restock: {disp.rma_id.name}',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.uom_id.id,
                    'location_id': disp.rma_id.partner_id.property_stock_customer.id,
                    'location_dest_id': disp.location_id.id or disp.warehouse_id.lot_stock_id.id,
                    'origin': disp.rma_id.name,
                })._action_done()

    def _action_repair(self):
        # Create repair order
        pass

    def _action_scrap(self):
        # Create scrap move
        pass


class RMACarrierLabel(models.Model):
    _name = 'rma.carrier.label'
    _description = 'RMA Carrier Label'

    rma_id = fields.Many2one('rma.request', string='RMA Request', required=True, ondelete='cascade')
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier', required=True)

    tracking_number = fields.Char(string='Tracking Number')
    label_file = fields.Binary(string='Label (PDF)', attachment=True)
    label_filename = fields.Char(string='Label Filename')
    cost = fields.Float(string='Label Cost')
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('printed', 'Printed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ], string='Status', default='draft')

    def action_generate(self):
        # Generate label via carrier API
        self.write({'state': 'generated', 'tracking_number': f'RMA-{self.rma_id.name}-{fields.Date.today()}'})