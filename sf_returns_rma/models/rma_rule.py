from odoo import _, api, fields, models


class RMARule(models.Model):
    _name = 'rma.rule'
    _description = 'RMA Auto-Approval Rule'
    _order = 'sequence, id'

    name = fields.Char(string='Rule Name', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    # Channel conditions
    channel_ids = fields.Many2many('rma.channel.config', string='Channels')
    country_ids = fields.Many2many('res.country', string='Countries')

    # Product conditions
    product_ids = fields.Many2many('product.product', string='Products')
    category_ids = fields.Many2many('product.category', string='Categories')

    # Customer conditions
    partner_ids = fields.Many2many('res.partner', string='Customers')
    partner_category_ids = fields.Many2many('res.partner.category', string='Customer Tags')

    # Value conditions
    min_amount = fields.Monetary(string='Min Amount', currency_field='currency_id')
    max_amount = fields.Monetary(string='Max Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)

    # Reason conditions
    reason_ids = fields.Many2many('rma.reason.config', string='Reasons')

    # Time conditions
    days_from_sale = fields.Integer(string='Max Days Since Sale')

    # Actions
    auto_approve = fields.Boolean(string='Auto-Approve', default=False)
    generate_label = fields.Boolean(string='Generate Return Label', default=False)
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')
    refund_type = fields.Selection([
        ('full', 'Full Refund'),
        ('partial', 'Partial (based on condition)'),
        ('store_credit', 'Store Credit'),
        ('exchange', 'Exchange Only'),
    ], string='Refund Type', default='full')

    def _match_request(self, rma):
        self.ensure_one()
        if self.channel_ids and rma.channel not in self.channel_ids.mapped('code'):
            return False
        if self.country_ids and rma.partner_id.country_id not in self.country_ids:
            return False
        if self.product_ids and not any(l.product_id in self.product_ids for l in rma.line_ids):
            return False
        if self.category_ids and not any(l.product_id.categ_id in self.category_ids for l in rma.line_ids):
            return False
        if self.partner_ids and rma.partner_id not in self.partner_ids:
            return False
        if self.partner_category_ids and not (rma.partner_id.category_id & self.partner_category_ids):
            return False
        if self.min_amount and rma.total_refund < self.min_amount:
            return False
        if self.max_amount and rma.total_refund > self.max_amount:
            return False
        if self.reason_ids and rma.reason not in self.reason_ids.mapped('code'):
            return False
        if self.days_from_sale and rma.sale_order_id:
            days = (fields.Date.today() - rma.sale_order_id.date_order.date()).days
            if days > self.days_from_sale:
                return False
        return True

    @api.model
    def _find_matching_rule(self, rma):
        rules = self.search([('active', '=', True)]).sorted('sequence')
        for rule in rules:
            if rule._match_request(rma):
                return rule
        return self.env['rma.rule']


class RMAChannelConfig(models.Model):
    _name = 'rma.channel.config'
    _description = 'RMA Channel Configuration'

    name = fields.Char(string='Channel Name', required=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(default=True)
    policy_days = fields.Integer(string='Policy Days', default=30)
    auto_approve_default = fields.Boolean(default=False)


class RMAReasonConfig(models.Model):
    _name = 'rma.reason.config'
    _description = 'RMA Reason Configuration'

    name = fields.Char(string='Reason Name', required=True)
    code = fields.Char(string='Code', required=True)
    active = fields.Boolean(default=True)
    requires_inspection = fields.Boolean(default=True)


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'rma.disposition'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
