# -*- coding: utf-8 -*-
"""Duplicate detection scans."""
from collections import defaultdict

from odoo import api, fields, models, _


class SfDedupScan(models.Model):
    _name = 'sf.dedup.scan'
    _description = 'Duplicate Scan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Scan', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    strategy = fields.Selection([
        ('exact_name', 'Exact Same Name'),
        ('name_city', 'Same Name + City'),
        ('same_vat', 'Same VAT Number'),
        ('same_email', 'Same Email')], required=True, default='exact_name')
    group_ids = fields.One2many('sf.dedup.group', 'scan_id',
                                string='Duplicate Groups')
    group_count = fields.Integer(compute='_compute_counts')
    open_count = fields.Integer(compute='_compute_counts')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Scanned')],
                             default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.dedup.scan') or 'DEDUP-NEW'
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.group_count = len(rec.group_ids)
            rec.open_count = len(rec.group_ids.filtered(
                lambda g: g.state == 'open'))

    def action_scan(self):
        self.ensure_one()
        self.group_ids.unlink()
        Partner = self.env['res.partner']
        partners = Partner.search([('company_id', 'in',
                                    [self.company_id.id, False])])
        buckets = defaultdict(list)
        if self.strategy == 'exact_name':
            for p in partners:
                buckets[(p.name or '').strip().lower()].append(p)
        elif self.strategy == 'name_city':
            for p in partners:
                buckets[(('%s|%s' % (p.name, p.city or '')).strip().lower())
                        ].append(p)
        elif self.strategy == 'same_vat':
            for p in partners:
                if p.vat:
                    buckets[p.vat.replace(' ', '').upper()].append(p)
        elif self.strategy == 'same_email':
            for p in partners:
                if p.email:
                    buckets[p.email.strip().lower()].append(p)
        vals_list = []
        for key, members in buckets.items():
            if len(members) < 2:
                continue
            vals_list.append({
                'scan_id': self.id,
                'match_key': key[:100],
                'record_count': len(members),
                'record_names': ', '.join(m.name for m in members)[:500],
            })
        if vals_list:
            self.env['sf.dedup.group'].create(vals_list)
        self.write({'state': 'done'})


class SfDedupGroup(models.Model):
    _name = 'sf.dedup.group'
    _description = 'Duplicate Group'

    scan_id = fields.Many2one('sf.dedup.scan', string='Scan', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one(related='scan_id.company_id', store=True)
    match_key = fields.Char(string='Match Key', readonly=True)
    record_count = fields.Integer(string='Duplicates', readonly=True)
    record_names = fields.Char(string='Records', readonly=True)
    state = fields.Selection([
        ('open', 'Open'), ('merged', 'Merged'), ('ignored', 'Ignored')],
        default='open')
    notes = fields.Text(string='Reviewer Notes')

    def action_mark_merged(self):
        self.write({'state': 'merged'})

    def action_ignore(self):
        self.write({'state': 'ignored'})

    def action_reopen(self):
        self.write({'state': 'open'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.dedup.scan'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
