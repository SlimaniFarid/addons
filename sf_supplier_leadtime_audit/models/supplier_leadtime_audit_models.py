# -*- coding: utf-8 -*-
"""Supplier Lead Time Audit models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_leadtime_audit(models.Model):
    _name = 'sf.supplier_leadtime_audit'
    _description = 'Supplier Lead Time Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quoted_days = fields.Integer(string='Quoted Lead (days)')
    actual_days = fields.Integer(string='Actual Lead (days)')
    variance_days = fields.Integer(string='Variance')
    rating = fields.Selection([
        ('good', 'Good'),
        ('acceptable', 'Acceptable'),
        ('poor', 'Poor'),
        ], string='Rating', default=acceptable)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier_leadtime_audit') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier_leadtime_audit'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave2 ---
class _Wave2Leadtime(models.Model):
    _inherit = 'sf.supplier_leadtime_audit'

    def action_import_from_po(self):
        """Promised vs actual lead time straight from purchase orders and
        their receipt pickings (needs purchase + stock apps)."""
        self.ensure_one()
        if not self.vendor_id or not self.product_id:
            return True
        PO = self.env['purchase.order.line']
        pos = PO.search([
            ('partner_id', '=', self.vendor_id.id),
            ('product_id', '=', self.product_id.id),
            ('state', 'in', ('purchase', 'done')),
        ], limit=50, order='date_order desc')
        quoted = actual = None
        for pol in pos:
            po = pol.order_id
            promised = (pol.date_planned.date() - po.date_order.date()).days
            receipts = po.picking_ids.filtered(
                lambda p: p.state == 'done'
                and any(m.product_id == self.product_id
                        for m in p.move_ids))
            if not receipts:
                continue
            first_done = min(receipts.mapped('date_deadline') or
                             receipts.mapped('scheduled_date'))
            eff = min(p.date_of_done for p in receipts)
            eff_date = fields.Date.to_date(eff)
            act = (eff_date - po.date_order.date()).days
            quoted, actual = promised, act
            break
        if quoted is None:
            self.notes = 'No received PO found for this couple.'
            return True
        variance = actual - quoted
        rating = 'good' if variance <= 0 else \
                 'fair' if variance <= 3 else 'poor'
        self.write({'quoted_days': quoted, 'actual_days': actual,
                    'variance_days': variance, 'rating': rating})
        return True
