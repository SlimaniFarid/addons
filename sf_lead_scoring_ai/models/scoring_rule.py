# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ScoringRule(models.Model):
    _name = 'sf.lead.scoring.ai.scoring.rule'
    _description = 'Scoring Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 store=True,
                                 default=lambda self: self.env.company)

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name', required=True)
    field_name = fields.Char(
        string='Lead Field', required=True,
        help='Technical name of a crm.lead field (e.g. email_from, '
             'expected_revenue, phone). Dot notation is not supported.')
    operator = fields.Selection([
        ('eq', '='), ('ne', '!='), ('gt', '>'), ('gte', '>='),
        ('lt', '<'), ('lte', '<='), ('contains', 'contains'),
    ], string='Operator', default='eq', required=True)
    score_value = fields.Integer(
        string='Expected Value / Points',
        help='Value the lead field is compared to. Also the number of '
             'points granted when the rule matches.')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.lead.scoring.ai.scoring.rule') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()

    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    # ------------------------------------------------------------- evaluation
    def _matches(self, lead):
        """True when lead.field_name <operator> score_value holds."""
        self.ensure_one()
        fname = (self.field_name or '').strip()
        if not fname or '.' in fname or fname not in lead._fields:
            return False
        value = lead[fname]
        expected = self.score_value

        def as_float(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        op = self.operator
        if op == 'contains':
            hay = str(getattr(value, 'display_name', '') or value or '').lower()
            return str(expected) in hay or bool(value) and str(expected) == ''
        if isinstance(value, bool):
            left = int(value)
        elif isinstance(value, (int, float)):
            left = value
        elif isinstance(value, models.Model):
            left = value.id
        else:
            text = str(value or '')
            if op in ('eq', 'ne'):
                eq = text == str(expected)
                return eq if op == 'eq' else not eq
            num = as_float(text)
            if num is None:
                return False
            left = num
        if op == 'eq':
            return left == expected
        if op == 'ne':
            return left != expected
        if op == 'gt':
            return left > expected
        if op == 'gte':
            return left >= expected
        if op == 'lt':
            return left < expected
        if op == 'lte':
            return left <= expected
        return False

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.lead.scoring.ai.lead.score'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

