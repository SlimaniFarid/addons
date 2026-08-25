# -*- coding: utf-8 -*-
"""Customer Document Vault models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerDoc(models.Model):
    _name = 'sf.customer.doc'
    _description = 'Customer Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    doc_type = fields.Selection([
        ('contract', 'Signed Contract'),
        ('insurance', 'Insurance Certificate'),
        ('audit', 'Audit Report'),
        ('compliance', 'Compliance Cert'),
        ('other', 'Other'),
        ], string='Document Type', required=True)
    received_date = fields.Date(string='Received')
    expiry_date = fields.Date(string='Expiry')
    attachment_ids = fields.Char(string='Files')
    chase_date = fields.Date(string='Chase Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('missing', 'Missing'),
        ('received', 'Received'),
        ('expired', 'Expired'),
        ], string='Status', default='missing', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.doc') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_expired(self):
        self.write({'state': 'expired'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer.doc'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

