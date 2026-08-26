# -*- coding: utf-8 -*-
"""Scrap Reason Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfScrapReason(models.Model):
    _name = 'sf.scrap.reason'
    _description = 'Scrap Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order')
    product_id = fields.Many2one('product.product', string='Product Scrapped', required=True)
    quantity = fields.Float(string='Qty Scrapped')
    reason_code = fields.Selection([
        ('setup', 'Setup Scrap'),
        ('defect', 'Defect'),
        ('material', 'Material Defect'),
        ('machine', 'Machine Fault'),
        ('operator', 'Operator Error'),
        ('other', 'Other'),
        ], string='Reason Code', required=True)
    cost = fields.Monetary(string='Scrap Cost')
    action_ref = fields.Char(string='Improvement Action Ref')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.scrap.reason') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.scrap.reason'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2ScrapImport(models.Model):
    _inherit = 'sf.scrap.reason'

    def action_import_from_stock(self):
        """One analytics row per native stock.scrap not yet imported
        (match on origin/product/qty)."""
        Scrap = self.env['stock.scrap']
        existing_keys = {
            (r.product_id.id, round(r.quantity, 2))
            for r in self.search([])}
        created = 0
        for sc in Scrap.search([], order='create_date desc', limit=200):
            key = (sc.product_id.id, round(sc.scrap_qty, 2))
            if key in existing_keys:
                continue
            reason = getattr(sc, 'scrap_reason_id', False)
            code = reason.name if reason else 'unspecified'
            self.create({
                'product_id': sc.product_id.id,
                'production_id': sc.production_id.id if hasattr(
                    sc, 'production_id') and sc.production_id else False,
                'quantity': sc.scrap_qty,
                'action_ref': sc.name,
            })
            existing_keys.add(key)
            created += 1
        self.message_post(body=_('Imported %s scrap record(s).') % created)
        return True
