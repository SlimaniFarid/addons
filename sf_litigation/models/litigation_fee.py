# -*- coding: utf-8 -*-
from odoo import api, fields, models


class LitigationFee(models.Model):
    _name = 'sf.litigation.fee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Litigation Fee'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, index=True)
    case_id = fields.Many2one('sf.litigation.case', string='Case',
                              required=True, ondelete='cascade', index=True)
    fee_type = fields.Selection([
        ('lawyer', 'Lawyer fees'),
        ('court', 'Court costs'),
        ('expert', 'Expert fees'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ], string='Fee type', required=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', required=True)
    paid = fields.Boolean(string='Paid', default=False)
    note = fields.Text(string='Note')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.litigation.fee')
            vals['name'] = 'FEE-%s' % seq
        return super().create(vals)