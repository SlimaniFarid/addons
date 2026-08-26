# -*- coding: utf-8 -*-
"""Min/Max Parameter Review models"""
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMinmaxReview(models.Model):
    _name = 'sf.minmax.review'
    _description = 'Min/Max Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    current_min = fields.Float(string='Current Min')
    current_max = fields.Float(string='Current Max')
    proposed_min = fields.Float(string='Proposed Min')
    proposed_max = fields.Float(string='Proposed Max')
    evidence = fields.Text(string='Demand Evidence')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ], string='Status', default='proposed', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.minmax.review') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_applied(self):
        self.write({'state': 'applied'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.minmax.review'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2MinMax(models.Model):
    _inherit = 'sf.minmax.review'

    def action_propose_from_usage(self):
        """Proposed min/max from real outbound usage:
        min = avg daily usage over 7d x cover_days_min
        max = avg daily usage over 28d x cover_days_max."""
        self.ensure_one()
        if not self.product_id:
            return True
        StockMove = self.env['stock.move']

        def avg_daily(days_back):
            frm = fields.Date.context_today(self) - relativedelta(
                days=days_back)
            moves = StockMove.search([
                ('product_id', '=', self.product_id.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm),
            ])
            qty = sum(m.product_uom.qty for m in moves)
            return qty / days_back

        d7, d28 = avg_daily(7), avg_daily(28)
        pmin = round(d7 * (self.cover_days_min or 7), 2)
        pmax = round(max(d28, d7) * (self.cover_days_max or 30), 2)
        self.write({
            'proposed_min': pmin,
            'proposed_max': pmax,
            'evidence': (_('Usage 7d/day=%.2f ; 28d/day=%.2f ; '
                           'cover=%sd/%sd') % (d7, d28,
                                               self.cover_days_min,
                                               self.cover_days_max)),
        })
        return True
