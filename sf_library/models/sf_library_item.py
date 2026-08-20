# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfLibraryItem(models.Model):
    _name = 'sf.library.item'
    _description = 'Library Item'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, tracking=True)
    reference = fields.Char(string='Reference', required=True, index=True)
    author = fields.Char(string='Author', tracking=True)
    media_type = fields.Selection([
        ('book', 'Book'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
        ('game', 'Game'),
        ('press', 'Press'),
        ('other', 'Other'),
    ], string='Media type', default='book', required=True, tracking=True)
    category_id = fields.Many2one(
        'sf.library.category', string='Category', ondelete='restrict',
        index=True, tracking=True)
    isbn = fields.Char(string='ISBN')
    language = fields.Char(string='Language')
    total_copies = fields.Integer(
        string='Total copies', default=1, required=True, tracking=True)
    available_copies = fields.Integer(
        string='Available copies', compute='_compute_available_copies',
        store=True)
    loan_ids = fields.One2many('sf.library.loan', 'item_id', string='Loans')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('total_copies', 'loan_ids.state')
    def _compute_available_copies(self):
        for item in self:
            item.available_copies = item.total_copies - len(
                item.loan_ids.filtered(lambda l: l.state == 'on_loan'))

    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'sf.library.item')
        return super().create(vals)
