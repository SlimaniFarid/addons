# -*- coding: utf-8 -*-
"""Scrap Pareto Analyzer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_scrap_pareto(models.Model):
    _name = 'sf.production_scrap_pareto'
    _description = 'Scrap Pareto Analyzer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    scrap_reason = fields.Char(string='Scrap Reason', required=True)
    quantity = fields.Float(string='Qty Scrapped')
    cost = fields.Monetary(string='Cost')
    cumulative_percent = fields.Float(string='Cumulative %')
    action_ref = fields.Char(string='Improvement Action')
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
                    'sf.production_scrap_pareto') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.production_scrap_pareto'

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
class _Wave2Pareto(models.Model):
    _inherit = 'sf.production_scrap_pareto'

    def action_build_pareto(self):
        """Aggregate native stock.scrap by product over all history,
        ordered desc quantity with cumulative % (80/20)."""
        self.ensure_one()
        Scrap = self.env['stock.scrap']
        groups = Scrap._read_group(
            [], ['product_id'], aggregates=['scrap_qty:sum'])
        rows = sorted(
            ((p.display_name, q or 0.0) for p, q in groups),
            key=lambda x: -x[1])
        total = sum(q for _, q in rows) or 1.0
        lines = []
        cum = 0.0
        Rank = 0
        for prod_name, qty in rows:
            Rank += 1
            share = qty / total * 100.0
            cum += share
            lines.append({
                'name': '%s-%02d' % (self.period or 'ALL', Rank),
                'period': self.period or 'ALL',
                'scrap_reason': prod_name,
                'quantity': qty,
                'cost': 0.0,
                'cumulative_percent': round(cum, 1),
            })
        self.search([('company_id', '=', self.company_id.id)]).unlink()
        self.create(lines)
        self.message_post(body=_('Pareto rebuilt: %s buckets, total qty %.2f.')
                          % (len(lines), total))
        return True
