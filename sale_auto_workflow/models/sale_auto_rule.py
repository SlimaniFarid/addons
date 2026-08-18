from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleAutoRule(models.Model):
    _name = 'sale.auto.rule'
    _description = 'Sales Automatic Workflow Rule'
    _order = 'sequence, id'

    name = fields.Char(string='Rule Name', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')

    # Conditions
    condition_type = fields.Selection([
        ('all', 'All Conditions'),
        ('any', 'Any Condition'),
    ], string='Match', default='all', required=True)

    payment_method_ids = fields.Many2many('account.payment.method', string='Payment Methods')
    sale_type_ids = fields.Many2many('sale.order.type', string='Order Types')
    partner_ids = fields.Many2many('res.partner', string='Customers')
    partner_category_ids = fields.Many2many('res.partner.category', string='Customer Tags')
    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    amount_min = fields.Monetary(string='Min Amount', currency_field='currency_id')
    amount_max = fields.Monetary(string='Max Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    user_ids = fields.Many2many('res.users', string='Salespersons')
    team_ids = fields.Many2many('crm.team', string='Sales Teams')
    country_ids = fields.Many2many('res.country', string='Customer Countries')
    state_ids = fields.Many2many('res.country.state', string='Customer States')

    # Actions
    action_confirm = fields.Boolean(string='Auto Confirm Order', default=True)
    action_create_delivery = fields.Boolean(string='Auto Create Delivery', default=False)
    action_validate_delivery = fields.Boolean(string='Auto Validate Delivery', default=False)
    action_create_invoice = fields.Boolean(string='Auto Create Invoice', default=False)
    action_post_invoice = fields.Boolean(string='Auto Post Invoice', default=False)
    action_send_email = fields.Boolean(string='Send Confirmation Email', default=False)
    email_template_id = fields.Many2one('mail.template', string='Email Template')

    rule_log_ids = fields.One2many('sale.auto.rule.log', 'rule_id', string='Execution Logs')

    def _match_order(self, order):
        self.ensure_one()
        checks = []

        if self.payment_method_ids:
            checks.append(order.payment_method_id.id in self.payment_method_ids.ids)
        if self.sale_type_ids:
            checks.append(order.type_id.id in self.sale_type_ids.ids if order.type_id else False)
        if self.partner_ids:
            checks.append(order.partner_id.id in self.partner_ids.ids)
        if self.partner_category_ids:
            checks.append(bool(order.partner_id.category_id & self.partner_category_ids))
        if self.warehouse_ids:
            checks.append(order.warehouse_id.id in self.warehouse_ids.ids if order.warehouse_id else False)
        if self.amount_min:
            checks.append(order.amount_total >= self.amount_min)
        if self.amount_max:
            checks.append(order.amount_total <= self.amount_max)
        if self.user_ids:
            checks.append(order.user_id.id in self.user_ids.ids if order.user_id else False)
        if self.team_ids:
            checks.append(order.team_id.id in self.team_ids.ids if order.team_id else False)
        if self.country_ids:
            checks.append(order.partner_id.country_id.id in self.country_ids.ids if order.partner_id.country_id else False)
        if self.state_ids:
            checks.append(order.partner_id.state_id.id in self.state_ids.ids if order.partner_id.state_id else False)

        if not checks:
            return False
        if self.condition_type == 'all':
            return all(checks)
        return any(checks)

    def apply(self, order):
        self.ensure_one()
        if not self._match_order(order):
            return False

        log_vals = {
            'rule_id': self.id,
            'order_id': order.id,
            'action': '',
            'status': 'success',
        }

        try:
            if self.action_confirm and order.state in ('draft', 'sent'):
                order.action_confirm()
                log_vals['action'] = 'confirm'
                self.env['sale.auto.rule.log'].create(log_vals)

            if self.action_create_delivery and order.state == 'sale':
                pickings = order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
                if pickings:
                    pickings.action_confirm()
                    pickings.action_assign()
                log_vals['action'] = 'create_delivery'
                self.env['sale.auto.rule.log'].create(log_vals)

            if self.action_validate_delivery and order.state == 'sale':
                for picking in order.picking_ids.filtered(lambda p: p.state in ('assigned', 'confirmed')):
                    for move in picking.move_ids_without_package:
                        move.quantity = move.product_uom_qty
                    picking.button_validate()
                log_vals['action'] = 'validate_delivery'
                self.env['sale.auto.rule.log'].create(log_vals)

            if self.action_create_invoice and order.state == 'sale':
                invoices = order._create_invoices()
                log_vals['action'] = 'create_invoice'
                self.env['sale.auto.rule.log'].create(log_vals)
                if self.action_post_invoice and invoices:
                    invoices.action_post()
                    log_vals['action'] = 'post_invoice'
                    self.env['sale.auto.rule.log'].create(log_vals)

            if self.action_send_email and self.email_template_id:
                self.email_template_id.send_mail(order.id, force_send=True)
                log_vals['action'] = 'send_email'
                self.env['sale.auto.rule.log'].create(log_vals)

        except Exception as e:
            log_vals['status'] = 'error'
            log_vals['error_message'] = str(e)
            self.env['sale.auto.rule.log'].create(log_vals)
            raise

        return True


class SaleAutoRuleLog(models.Model):
    _name = 'sale.auto.rule.log'
    _description = 'Sales Auto Rule Execution Log'
    _order = 'create_date desc'

    rule_id = fields.Many2one('sale.auto.rule', string='Rule', required=True, ondelete='cascade')
    order_id = fields.Many2one('sale.order', string='Order', required=True, ondelete='cascade')
    action = fields.Char(string='Action')
    status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
    ], string='Status', default='success')
    error_message = fields.Text(string='Error Message')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    auto_rule_applied_ids = fields.Many2many('sale.auto.rule', string='Applied Rules', readonly=True)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            rules = self.env['sale.auto.rule'].search([
                ('active', '=', True),
            ]).sorted('sequence')
            for rule in rules:
                if rule.id not in order.auto_rule_applied_ids.ids:
                    try:
                        rule.apply(order)
                        order.auto_rule_applied_ids = [(4, rule.id)]
                    except Exception:
                        pass
        return res