# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LeadScore(models.Model):
    _name = 'sf.lead.scoring.ai.lead.score'
    _description = 'Lead Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'total_score desc, id desc'
    _rec_name = 'lead_id'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 store=True, default=lambda self: self.env.company)

    lead_id = fields.Many2one(required=True, comodel_name='crm.lead',
                              ondelete='restrict')
    total_score = fields.Integer(string='Total Score', tracking=True)
    grade = fields.Selection([
        ('A', 'Grade A (>=75)'), ('B', 'Grade B (>=50)'),
        ('C', 'Grade C (>=25)'), ('D', 'Grade D (<25)'),
    ], string='Grade', default='D', tracking=True)
    scored_date = fields.Datetime(string='Scored Date',
                                  default=fields.Datetime.now)
    matched_rule_ids = fields.Many2many(
        'sf.lead.scoring.ai.scoring.rule',
        'lead_score_rule_rel', 'score_id', 'rule_id',
        string='Matched Rules', readonly=True)

    _sql_constraints = [
        ('lead_uniq', 'unique(lead_id)',
         'One score record per lead.'),
    ]

    # ------------------------------------------------------------------ engine
    def _grade_for(self, score):
        if score >= 75:
            return 'A'
        if score >= 50:
            return 'B'
        if score >= 25:
            return 'C'
        return 'D'

    def _evaluate_rules(self, lead):
        """Evaluate every active rule against the lead. Returns (score, rules)."""
        Rule = self.env['sf.lead.scoring.ai.scoring.rule']
        score = 0
        matched = self.env['sf.lead.scoring.ai.scoring.rule']
        for rule in Rule.search([('active', '=', True)]):
            if rule._matches(lead):
                score += rule.score_value
                matched |= rule
        return score, matched

    def action_recompute(self):
        for rec in self:
            if not rec.lead_id:
                continue
            score, matched = rec._evaluate_rules(rec.lead_id)
            rec.write({
                'total_score': score,
                'grade': rec._grade_for(score),
                'scored_date': fields.Datetime.now(),
                'matched_rule_ids': [(6, 0, matched.ids)],
            })
            rec.message_post(body=_(
                'Score recomputed: %s points (grade %s), %s rule(s) matched.')
                % (score, rec.grade, len(matched)))
        return True

    @api.model
    def action_score_all_leads(self):
        """Score every open CRM lead (cron entry point / manual run)."""
        Lead = self.env['crm.lead']
        leads = Lead.search([('probability', '<', 100)])
        created = 0
        for lead in leads:
            score_rec = self.search([('lead_id', '=', lead.id)], limit=1)
            if not score_rec:
                score_rec = self.create({'lead_id': lead.id})
                created += 1
            score_rec.with_context(skip_recompute_guard=True).action_recompute()
            # auto-prioritisation promised by the module: push hot leads up
            if score_rec.grade == 'A' and lead.priority != '3':
                lead.priority = '3'
            elif score_rec.grade == 'B' and lead.priority in ('1', False):
                lead.priority = '2'
        message = _('Scoring done: %s lead(s) scored (%s new).')
        self.message_post(body=message % (len(leads), created))
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('Lead Scoring'),
                       'message': message % (len(leads), created),
                       'type': 'success'},
        }
