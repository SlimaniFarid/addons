import re
import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class BarcodeConfig(models.Model):
    _name = 'barcode.config'
    _description = 'Barcode Configuration'
    _order = 'sequence'

    name = fields.Char(string='Configuration Name', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    # Supported patterns
    pattern_product = fields.Char(string='Product Pattern', default='^\\d{12,14}$',
        help='Regex for product barcodes (EAN13, UPC, etc.)')
    pattern_lot = fields.Char(string='Lot/Serial Pattern', default='^LOT-\\d+$')
    pattern_package = fields.Char(string='Package Pattern', default='^PKG-\\d+$')
    pattern_location = fields.Char(string='Location Pattern', default='^LOC-\\d+$')
    pattern_gs1 = fields.Char(string='GS1 Pattern', default='^\\(01\\)\\d{14}\\(10\\)',
        help='GS1 Application Identifiers: (01)=GTIN, (10)=Lot, (21)=Serial, (30)=Qty')

    # Behavior
    auto_create_lot = fields.Boolean(string='Auto Create Lot/Serial', default=True)
    auto_create_package = fields.Boolean(string='Auto Create Package', default=True)
    default_location_id = fields.Many2one('stock.location', string='Default Scan Location')
    allowed_operation_types = fields.Many2many(
        'stock.picking.type', string='Allowed Operations',
        help='Limit scanning to these operation types')

    company_id = fields.Many2one('res.company', string='Company', default=lambda s: s.env.company)

    def parse_barcode(self, barcode):
        self.ensure_one()
        if re.match(self.pattern_gs1, barcode):
            return self._parse_gs1(barcode)
        if re.match(self.pattern_product, barcode):
            return {'type': 'product', 'code': barcode}
        if re.match(self.pattern_lot, barcode):
            return {'type': 'lot', 'code': barcode}
        if re.match(self.pattern_package, barcode):
            return {'type': 'package', 'code': barcode}
        if re.match(self.pattern_location, barcode):
            return {'type': 'location', 'code': barcode}
        # Try product by barcode field
        product = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        if product:
            return {'type': 'product', 'code': barcode, 'product_id': product.id}
        return {'type': 'unknown', 'code': barcode}

    def _parse_gs1(self, barcode):
        # Simplified GS1 parser
        result = {'type': 'gs1', 'raw': barcode}
        # (01) GTIN
        m = re.search(r'\(01\)(\d{14})', barcode)
        if m:
            result['gtin'] = m.group(1)
        # (10) Lot
        m = re.search(r'\(10\)([^\)]+)', barcode)
        if m:
            result['lot'] = m.group(1)
        # (21) Serial
        m = re.search(r'\(21\)([^\)]+)', barcode)
        if m:
            result['serial'] = m.group(1)
        # (30) Qty
        m = re.search(r'\(30\)(\d+)', barcode)
        if m:
            result['qty'] = int(m.group(1))
        return result


class BarcodeScan(models.TransientModel):
    _name = 'barcode.scan'
    _description = 'Barcode Scan Wizard'

    config_id = fields.Many2one('barcode.config', string='Configuration', required=True,
        default=lambda s: s.env['barcode.config'].search([('active', '=', True)], limit=1))
    picking_id = fields.Many2one('stock.picking', string='Picking', required=True)
    barcode = fields.Char(string='Barcode', required=True)
    parsed_data = fields.Text(string='Parsed Data', readonly=True)
    action = fields.Selection([
        ('scan_product', 'Scan Product'),
        ('scan_lot', 'Scan Lot/Serial'),
        ('scan_package', 'Scan Package'),
        ('scan_location', 'Scan Location'),
        ('scan_gs1', 'Scan GS1'),
    ], string='Action', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial', readonly=True)
    package_id = fields.Many2one('stock.quant.package', string='Package', readonly=True)
    location_id = fields.Many2one('stock.location', string='Location', readonly=True)
    quantity = fields.Float(string='Quantity', default=1.0)

    def action_scan(self):
        self.ensure_one()
        config = self.config_id
        parsed = config.parse_barcode(self.barcode)
        self.write({'parsed_data': str(parsed)})

        if parsed['type'] == 'product':
            self.action = 'scan_product'
            product = self.env['product.product'].search([('barcode', '=', self.barcode)], limit=1)
            if not product and parsed.get('gtin'):
                product = self.env['product.product'].search([('barcode', '=', parsed['gtin'])], limit=1)
            self.product_id = product.id
            if product:
                self._add_move_line(product)
        elif parsed['type'] == 'lot':
            self.action = 'scan_lot'
            lot = self.env['stock.lot'].search([('name', '=', parsed['code'])], limit=1)
            if not lot and config.auto_create_lot:
                lot = self.env['stock.lot'].create({
                    'name': parsed['code'],
                    'product_id': self.product_id.id or self.picking_id.move_ids[0].product_id.id,
                })
            self.lot_id = lot.id
        elif parsed['type'] == 'package':
            self.action = 'scan_package'
            package = self.env['stock.quant.package'].search([('name', '=', parsed['code'])], limit=1)
            if not package and config.auto_create_package:
                package = self.env['stock.quant.package'].create({'name': parsed['code']})
            self.package_id = package.id
        elif parsed['type'] == 'location':
            self.action = 'scan_location'
            location = self.env['stock.location'].search([('name', '=', parsed['code'])], limit=1)
            self.location_id = location.id
        elif parsed['type'] == 'gs1':
            self.action = 'scan_gs1'
            if parsed.get('gtin'):
                product = self.env['product.product'].search([('barcode', '=', parsed['gtin'])], limit=1)
                self.product_id = product.id
            if parsed.get('lot'):
                lot = self.env['stock.lot'].search([('name', '=', parsed['lot'])], limit=1)
                if not lot and config.auto_create_lot and self.product_id:
                    lot = self.env['stock.lot'].create({
                        'name': parsed['lot'],
                        'product_id': self.product_id.id,
                    })
                self.lot_id = lot.id
            if parsed.get('qty'):
                self.quantity = parsed['qty']
            if self.product_id:
                self._add_move_line(self.product_id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'barcode.scan',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def _add_move_line(self, product):
        self.ensure_one()
        picking = self.picking_id
        move = picking.move_ids.filtered(lambda m: m.product_id == product)
        if not move:
            move = self.env['stock.move'].create({
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': self.quantity,
                'product_uom': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
            })
        else:
            move.write({'product_uom_qty': move.product_uom_qty + self.quantity})

        ml_vals = {
            'move_id': move.id,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'quantity': self.quantity,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'picking_id': picking.id,
        }
        if self.lot_id:
            ml_vals['lot_id'] = self.lot_id.id
        if self.package_id:
            ml_vals['package_id'] = self.package_id.id
        if self.location_id:
            ml_vals['location_id'] = self.location_id.id

        self.env['stock.move.line'].create(ml_vals)

    def action_done(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}


class BarcodeLog(models.Model):
    _name = 'barcode.log'
    _description = 'Barcode Scan Log'
    _order = 'create_date desc'

    config_id = fields.Many2one('barcode.config', string='Configuration', ondelete='set null')
    user_id = fields.Many2one('res.users', string='User', default=lambda s: s.env.user)
    picking_id = fields.Many2one('stock.picking', string='Picking', ondelete='set null')
    barcode = fields.Char(string='Barcode', required=True)
    parsed_type = fields.Char(string='Parsed Type')
    action = fields.Char(string='Action')
    product_id = fields.Many2one('product.product', string='Product', ondelete='set null')
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial', ondelete='set null')
    package_id = fields.Many2one('stock.quant.package', string='Package', ondelete='set null')
    location_id = fields.Many2one('stock.location', string='Location', ondelete='set null')
    quantity = fields.Float(string='Quantity')
    success = fields.Boolean(string='Success', default=True)
    error_message = fields.Text(string='Error')

    @api.model
    def log_scan(self, config_id, picking_id, barcode, parsed, action, **kwargs):
        return self.create({
            'config_id': config_id,
            'picking_id': picking_id,
            'barcode': barcode,
            'parsed_type': parsed.get('type') if parsed else 'unknown',
            'action': action,
            **kwargs,
        })


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'barcode.config'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
