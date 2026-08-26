# -*- coding: utf-8 -*-
"""Supplier Questionnaire Campaigns models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierQuestionnaire(models.Model):
    _name = 'sf.supplier.questionnaire'
    _description = 'Questionnaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    questionnaire_type = fields.Selection([
        ('compliance', 'Compliance'),
        ('esg', 'ESG'),
        ('quality', 'Quality System'),
        ('cyber', 'Cybersecurity'),
        ], string='Type', required=True)
    sent_date = fields.Date(string='Sent', default=fields.Date.today)
    due_date = fields.Date(string='Response Due')
    score = fields.Float(string='Score (0-100)')
    follow_up = fields.Text(string='Follow-up')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('evaluated', 'Evaluated'),
        ('chased', 'Chased'),
        ], string='Status', default='sent', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.questionnaire') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_evaluated(self):
        self.write({'state': 'evaluated'})

    def action_chased(self):
        self.write({'state': 'chased'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier.questionnaire'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.supplier.questionnaire'

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
