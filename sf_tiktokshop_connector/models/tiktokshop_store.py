import hashlib
import hmac
import json
import logging
import time
import requests
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class TikTokShopStore(models.Model):
    _name = 'tiktokshop.store'
    _description = 'TikTok Shop Store'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Store Name', required=True)
    shop_id = fields.Char(string='Shop ID', required=True)
    shop_cipher = fields.Char(string='Shop Cipher', help='Encrypted shop identifier from TikTok')
    region = fields.Selection([
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('ID', 'Indonesia'),
        ('MY', 'Malaysia'),
        ('PH', 'Philippines'),
        ('SG', 'Singapore'),
        ('TH', 'Thailand'),
        ('VN', 'Vietnam'),
        ('SA', 'Saudi Arabia'),
    ], string='Region', required=True)

    app_key = fields.Char(string='App Key', required=True)
    app_secret = fields.Char(string='App Secret', required=True, groups='base.group_system')
    access_token = fields.Char(string='Access Token', required=True, groups='base.group_system')
    refresh_token = fields.Char(string='Refresh Token', groups='base.group_system')
    token_expires_at = fields.Datetime(string='Token Expires At')

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Not Connected'),
        ('connected', 'Connected'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True, readonly=True)

    sync_products = fields.Boolean(string='Sync Products', default=True)
    sync_inventory = fields.Boolean(string='Sync Inventory', default=True)
    sync_orders = fields.Boolean(string='Sync Orders', default=True)
    sync_returns = fields.Boolean(string='Sync Returns', default=True)

    product_ids = fields.One2many('tiktokshop.product', 'store_id', string='Products')
    order_ids = fields.One2many('tiktokshop.order', 'store_id', string='Orders')
    sync_log_ids = fields.One2many('tiktokshop.sync.log', 'store_id', string='Sync Logs')

    _sql_constraints = [
        ('shop_id_uniq', 'unique(shop_id)', 'Shop ID must be unique.'),
    ]

    def _get_base_url(self):
        return 'https://open-api.tiktokglobalshop.com'

    def _get_headers(self, path, query_params, body=''):
        self.ensure_one()
        timestamp = str(int(time.time()))
        sign_string = f'{self.app_key}{timestamp}{path}{query_params}{body}'
        signature = hmac.new(
            self.app_secret.encode(), sign_string.encode(), hashlib.sha256
        ).hexdigest()
        return {
            'x-tts-access-token': self.access_token,
            'x-tts-timestamp': timestamp,
            'x-tts-sign': signature,
            'x-tts-app-key': self.app_key,
            'Content-Type': 'application/json',
        }

    def _request(self, method, path, params=None, data=None):
        self.ensure_one()
        url = self._get_base_url() + path
        query = '&'.join(f'{k}={v}' for k, v in sorted((params or {}).items()))
        body = json.dumps(data) if data else ''
        headers = self._get_headers(path, query, body)
        try:
            if method == 'GET':
                resp = requests.get(url, headers=headers, params=params, timeout=30)
            else:
                resp = requests.post(url, headers=headers, params=params, json=data, timeout=30)
            if resp.status_code == 401:
                # Token might be expired - could implement refresh here
                raise UserError('Token expired or invalid')
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            _logger.exception('TikTok Shop API error')
            raise UserError(f'API Error: {e}')

    def action_test_connection(self):
        for store in self:
            try:
                result = store._request('GET', '/authorization/202309/shops', params={'shop_cipher': store.shop_cipher})
                if result.get('code') == 0:
                    store.state = 'connected'
                else:
                    store.state = 'error'
            except Exception:
                store.state = 'error'

    def action_sync_products(self):
        self.ensure_one()
        return self._sync_products()

    def _sync_products(self):
        self.ensure_one()
        log = self.env['tiktokshop.sync.log'].create({
            'store_id': self.id,
            'operation': 'products',
            'direction': 'pull',
            'status': 'running',
        })
        try:
            page_token = ''
            total = 0
            while True:
                params = {'shop_cipher': self.shop_cipher, 'page_size': 50}
                if page_token:
                    params['page_token'] = page_token
                result = self._request('GET', '/product/202309/products/search', params=params)
                if result.get('code') != 0:
                    raise UserError(result.get('message', 'Unknown error'))
                products = result.get('data', {}).get('products', [])
                for prod in products:
                    self._create_or_update_product(prod)
                    total += 1
                page_token = result.get('data', {}).get('page_token', '')
                if not page_token:
                    break
            log.write({'status': 'success', 'records_processed': total})
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Success', 'message': f'Synced {total} products', 'type': 'success'}}
        except Exception as e:
            log.write({'status': 'error', 'error_message': str(e)})
            raise

    def _create_or_update_product(self, prod_data):
        tiktok_id = prod_data.get('id') or prod_data.get('product_id')
        existing = self.env['tiktokshop.product'].search([
            ('store_id', '=', self.id),
            ('tiktok_product_id', '=', tiktok_id),
        ], limit=1)
        vals = {
            'store_id': self.id,
            'tiktok_product_id': tiktok_id,
            'name': prod_data.get('title'),
            'description': prod_data.get('description'),
            'status': prod_data.get('status'),
            'category_id': prod_data.get('category_id'),
            'brand': prod_data.get('brand'),
            'images': json.dumps(prod_data.get('images', [])),
            'skus': json.dumps(prod_data.get('skus', [])),
        }
        if existing:
            existing.write(vals)
        else:
            self.env['tiktokshop.product'].create(vals)

    def _sync_inventory(self):
        self.ensure_one()
        log = self.env['tiktokshop.sync.log'].create({
            'store_id': self.id,
            'operation': 'inventory',
            'direction': 'push',
            'status': 'running',
        })
        # Implementation for pushing Odoo stock to TikTok
        log.write({'status': 'success', 'records_processed': 0})

    def _sync_orders(self):
        self.ensure_one()
        log = self.env['tiktokshop.sync.log'].create({
            'store_id': self.id,
            'operation': 'orders',
            'direction': 'pull',
            'status': 'running',
        })
        try:
            params = {'shop_cipher': self.shop_cipher, 'page_size': 50}
            result = self._request('GET', '/order/202309/orders/search', params=params)
            if result.get('code') != 0:
                raise UserError(result.get('message', 'Unknown error'))
            orders = result.get('data', {}).get('orders', [])
            total = 0
            for order in orders:
                self._create_or_update_order(order)
                total += 1
            log.write({'status': 'success', 'records_processed': total})
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Success', 'message': f'Synced {total} orders', 'type': 'success'}}
        except Exception as e:
            log.write({'status': 'error', 'error_message': str(e)})
            raise

    def _create_or_update_order(self, order_data):
        tiktok_id = order_data.get('id')
        existing = self.env['tiktokshop.order'].search([
            ('store_id', '=', self.id),
            ('tiktok_order_id', '=', tiktok_id),
        ], limit=1)
        vals = {
            'store_id': self.id,
            'tiktok_order_id': tiktok_id,
            'order_status': order_data.get('status'),
            'create_time': order_data.get('create_time'),
            'update_time': order_data.get('update_time'),
            'total_amount': order_data.get('total_amount'),
            'currency': order_data.get('currency'),
            'buyer_info': json.dumps(order_data.get('buyer', {})),
            'shipping_info': json.dumps(order_data.get('shipping', {})),
            'line_items': json.dumps(order_data.get('line_items', [])),
        }
        if existing:
            existing.write(vals)
        else:
            self.env['tiktokshop.order'].create(vals)


class TikTokShopProduct(models.Model):
    _name = 'tiktokshop.product'
    _description = 'TikTok Shop Product'
    _order = 'name'

    store_id = fields.Many2one('tiktokshop.store', string='Store', required=True, ondelete='cascade')
    tiktok_product_id = fields.Char(string='TikTok Product ID', required=True)
    name = fields.Char(string='Product Name')
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Review'),
        ('rejected', 'Rejected'),
    ], string='Status')
    category_id = fields.Char(string='Category ID')
    brand = fields.Char(string='Brand')
    images = fields.Text(string='Images (JSON)')
    skus = fields.Text(string='SKUs (JSON)')
    odoo_product_id = fields.Many2one('product.product', string='Odoo Product', ondelete='set null')

    _sql_constraints = [
        ('tiktok_product_store_uniq', 'unique(tiktok_product_id, store_id)', 'Product must be unique per store.'),
    ]


class TikTokShopOrder(models.Model):
    _name = 'tiktokshop.order'
    _description = 'TikTok Shop Order'
    _order = 'create_time desc'

    store_id = fields.Many2one('tiktokshop.store', string='Store', required=True, ondelete='cascade')
    tiktok_order_id = fields.Char(string='TikTok Order ID', required=True)
    order_status = fields.Selection([
        ('pending', 'Pending'),
        ('awaiting_shipment', 'Awaiting Shipment'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ], string='Status')
    create_time = fields.Datetime(string='Create Time')
    update_time = fields.Datetime(string='Update Time')
    total_amount = fields.Float(string='Total Amount')
    currency = fields.Char(string='Currency')
    buyer_info = fields.Text(string='Buyer Info (JSON)')
    shipping_info = fields.Text(string='Shipping Info (JSON)')
    line_items = fields.Text(string='Line Items (JSON)')
    odoo_order_id = fields.Many2one('sale.order', string='Odoo Order', ondelete='set null')

    _sql_constraints = [
        ('tiktok_order_store_uniq', 'unique(tiktok_order_id, store_id)', 'Order must be unique per store.'),
    ]


class TikTokShopSyncLog(models.Model):
    _name = 'tiktokshop.sync.log'
    _description = 'TikTok Shop Sync Log'
    _order = 'create_date desc'

    store_id = fields.Many2one('tiktokshop.store', string='Store', required=True, ondelete='cascade')
    operation = fields.Selection([
        ('products', 'Products'),
        ('inventory', 'Inventory'),
        ('orders', 'Orders'),
        ('returns', 'Returns'),
    ], string='Operation', required=True)
    direction = fields.Selection([
        ('push', 'Push to TikTok'),
        ('pull', 'Pull from TikTok'),
    ], string='Direction', required=True)
    status = fields.Selection([
        ('running', 'Running'),
        ('success', 'Success'),
        ('error', 'Error'),
    ], string='Status', default='running')
    records_processed = fields.Integer(string='Records Processed', default=0)
    error_message = fields.Text(string='Error Message')
    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time')