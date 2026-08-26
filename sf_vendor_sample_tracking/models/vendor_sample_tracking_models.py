# -*- coding: utf-8 -*-
"""Vendor Sample Request Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVendorSample(models.Model):
    _name = 'sf.vendor.sample'
    _description = 'Vendor Sample Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    product_desc = fields.Char(string='Sample Description', required=True)
    requested_date = fields.Date(string='Requested', default=fields.Date.today)
    received_date = fields.Date(string='Received')
    evaluation = fields.Text(string='Evaluation')
    approved_for_use = fields.Boolean(string='Approved for Use')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('received', 'Received'),
        ('evaluated', 'Evaluated'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.vendor.sample') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_evaluated(self):
        self.write({'state': 'evaluated'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.vendor.sample'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.vendor.sample'

    def action_refresh_business(self):
        """Pull PO count and total for linked vendor."""
        for rec in self:
            vendor = getattr(rec, 'vendor_id',
                             getattr(rec, 'partner_id', False))
            if not vendor:
                continue
            pos = self.env['purchase.order'].search([
                ('partner_id', '=', vendor.id),
                ('state', 'in', ('purchase', 'done'))])
            rec.message_post(body=_(
                '{n} confirmed PO(s), total {t:.2f}.').format(
                n=len(pos), t=sum(pos.mapped('amount_total'))))
        return True
