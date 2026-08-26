# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LitigationDecision(models.Model):
    _name = 'sf.litigation.decision'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Litigation Decision'
    _order = 'decision_date desc, id desc'

    name = fields.Char(string='Reference', required=True, index=True,
                       tracking=True)
    case_id = fields.Many2one('sf.litigation.case', string='Case',
                              required=True, ondelete='cascade', index=True)
    decision_date = fields.Date(string='Decision date', required=True,
                                tracking=True)
    outcome = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('partially_won', 'Partially won'),
        ('settled', 'Settled'),
        ('other', 'Other'),
    ], string='Outcome', required=True, tracking=True)
    amount_awarded = fields.Float(string='Amount awarded')
    summary = fields.Text(string='Summary')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('recorded', 'Recorded'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.litigation.decision')
            vals['name'] = 'DEC-%s' % seq
        return super().create(vals)

    def action_record(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft decisions can be recorded.'))
        self.state = 'recorded'