# -*- coding: utf-8 -*-
"""Price change campaigns."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPriceChange(models.Model):
    _name = 'sf.price.change'
    _description = 'Price Change Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'effective_date desc'

    name = fields.Char(string='Campaign', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    reason = fields.Selection([
        ('cost_increase', 'Raw Material Cost Increase'),
        ('market', 'Market Alignment'),
        ('fx', 'Currency Impact'),
        ('annual', 'Annual Review'),
        ('other', 'Other')], required=True, default='cost_increase')
    announcement_date = fields.Date(string='Announcement Date',
                                    default=fields.Date.today)
    effective_date = fields.Date(string='Effective Date', required=True)
    line_ids = fields.One2many('sf.price.change.line', 'change_id',
                               string='Products')
    line_count = fields.Integer(compute='_compute_stats')
    avg_delta = fields.Float(string='Average Delta %',
                             compute='_compute_stats')
    state = fields.Selection([
        ('draft', 'Draft'), ('announced', 'Announced'),
        ('applied', 'Applied'), ('cancelled', 'Cancelled')],
        default='draft', tracking=True, copy=False)
    applied_date = fields.Date(readonly=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.price.change') or 'PRC-NEW'
        return super().create(vals_list)

    def _compute_stats(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)
            rec.avg_delta = (sum(rec.line_ids.mapped('delta_percent')) /
                             rec.line_count if rec.line_count else 0.0)

    def action_announce(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Add product lines first.'))
        self.write({'state': 'announced'})

    def action_apply(self):
        self.ensure_one()
        if self.state != 'announced':
            raise UserError(_('Announce the campaign before applying.'))
        if fields.Date.context_today(self) < self.effective_date:
            raise UserError(_('Effective date not reached yet.'))
        for line in self.line_ids:
            line.old_price = line.product_id.list_price
            line.product_id.list_price = line.new_price
        self.write({'state': 'applied',
                    'applied_date': fields.Date.today()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfPriceChangeLine(models.Model):
    _name = 'sf.price.change.line'
    _description = 'Price Change Line'

    change_id = fields.Many2one('sf.price.change', string='Campaign',
                                required=True, ondelete='cascade')
    company_id = fields.Many2one(related='change_id.company_id', store=True)
    currency_id = fields.Many2one(related='change_id.currency_id')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    old_price = fields.Float(string='Current Price', readonly=True)
    new_price = fields.Float(string='New Price', required=True)
    delta_percent = fields.Float(string='Delta %',
                                 compute='_compute_delta', store=True)

    @api.depends('old_price', 'new_price')
    def _compute_delta(self):
        for line in self:
            line.delta_percent = ((line.new_price - line.old_price) /
                                  line.old_price * 100.0
                                  if line.old_price else 0.0)

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.old_price = self.product_id.list_price

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.price.change'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
