# -*- coding: utf-8 -*-
"""Late Payment Interest Calculator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLateInterest(models.Model):
    _name = 'sf.late.interest'
    _description = 'Late Interest Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rate_percent = fields.Float(string='Annual Rate %', default=5.0)
    grace_days = fields.Integer(string='Grace Days', default=30)
    as_of_date = fields.Date(string='As Of', default=fields.Date.today)
    total_interest = fields.Float(string='Total Interest')
    invoice_count = fields.Integer(string='Overdue Invoices')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('invoiced', 'Invoiced'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.late.interest') or 'NEW'
        return super().create(vals_list)

    def action_computed(self):
        self.write({'state': 'computed'})

    def action_invoiced(self):
        self.write({'state': 'invoiced'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.late.interest'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2(models.Model):
    _inherit = 'sf.late.interest'

    line_ids = fields.One2many('sf.late.interest.line', 'interest_id',
                               string='Detail Lines')

    def action_compute(self):
        """Real interest on overdue customer invoices:
        amount_residual * rate% * days_late / 365 (grace days excluded)."""
        self.ensure_one()
        Line = self.env['sf.late.interest.line']
        Line.search([('interest_id', '=', self.id)]).unlink()
        as_of = self.as_of_date or fields.Date.context_today(self)
        Move = self.env['account.move']
        invoices = Move.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ('not_paid', 'partial')),
            ('invoice_date_due', '<', as_of),
            ('company_id', '=', self.company_id.id),
        ])
        total, count = 0.0, 0
        vals_list = []
        for inv in invoices:
            days_late = (as_of - inv.invoice_date_due).days
            net_days = days_late - (self.grace_days or 0)
            if net_days <= 0 or not inv.amount_residual:
                continue
            interest = round(
                inv.amount_residual * (self.rate_percent / 100.0)
                * net_days / 365.0, 2)
            if interest <= 0:
                continue
            vals_list.append({
                'interest_id': self.id,
                'invoice_id': inv.id,
                'partner_name': inv.partner_id.display_name,
                'days_late': net_days,
                'residual': inv.amount_residual,
                'interest_amount': interest,
            })
            total += interest
            count += 1
        Line.create(vals_list)
        self.write({'total_interest': total, 'invoice_count': count})
        self.message_post(body=_(
            'Computed %(c)s overdue invoice(s): interest total %(t)s '
            '(rate %(r)s%%, grace %(g)s d).')
            % {'c': count, 't': total,
               'r': self.rate_percent, 'g': self.grace_days})
        return True


class LateInterestLine(models.Model):
    _name = 'sf.late.interest.line'
    _description = 'Late Payment Interest Detail'
    _order = 'days_late desc'

    interest_id = fields.Many2one('sf.late.interest', required=True,
                                  ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string='Invoice',
                                 ondelete='cascade')
    partner_name = fields.Char(string='Customer')
    days_late = fields.Integer(string='Days late (net)')
    residual = fields.Monetary(string='Open amount')
    interest_amount = fields.Monetary(string='Interest')
    currency_id = fields.Many2one(related='interest_id.currency_id')
