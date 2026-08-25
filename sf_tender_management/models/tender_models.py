# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Tender(models.Model):
    _name = 'sf.tender'
    _description = 'Tender'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    title = fields.Char(string='Title', required=True)
    tender_type = fields.Selection([
        ('rfq', 'RFQ (Request for Quote)'),
        ('rfi', 'RFI (Request for Information)'),
        ('rfp', 'RFP (Request for Proposal)'),
        ('public_tender', 'Public Tender'),
    ], string='Type', required=True)
    description = fields.Html(string='Description')
    buyer_id = fields.Many2one('res.users', string='Buyer',
                               default=lambda self: self.env.user,
                               required=True, ondelete='restrict')
    deadline = fields.Datetime(string='Submission deadline', required=True,
                               index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('in_evaluation', 'In Evaluation'),
        ('awarded', 'Awarded'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    winner_offer_id = fields.Many2one('sf.tender.offer',
                                      string='Winning offer')
    award_justification = fields.Text(string='Award justification')
    invited_partner_ids = fields.Many2many('res.partner',
                                           string='Invited suppliers')
    criterion_ids = fields.One2many('sf.tender.criterion', 'tender_id',
                                    string='Evaluation criteria')
    offer_ids = fields.One2many('sf.tender.offer', 'tender_id',
                                string='Offers')
    award_date = fields.Date(string='Award date')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This tender number already exists.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.tender')
            vals['name'] = 'TND-%s' % seq
        return super().create(vals)

    def action_publish(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft tenders can be published.'))
        self.state = 'published'

    def action_start_evaluation(self):
        self.ensure_one()
        if self.state != 'published':
            raise UserError(_('Only published tenders can be evaluated.'))
        now = fields.Datetime.now()
        if now < self.deadline:
            raise UserError(_('Evaluation cannot start before the '
                              'submission deadline.'))
        self.state = 'in_evaluation'

    def action_open_award_wizard(self):
        self.ensure_one()
        if self.state != 'in_evaluation':
            raise UserError(_('A tender can be awarded only while it is '
                              'being evaluated.'))
        if not self.offer_ids:
            raise UserError(_('There is no offer to award.'))
        return {
            'name': _('Award Tender'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.tender.award.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_tender_id': self.id},
        }

    def action_close(self):
        self.ensure_one()
        if self.state != 'awarded':
            raise UserError(_('Only awarded tenders can be closed.'))
        self.state = 'closed'
        self.active = False

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ('draft', 'published'):
            raise UserError(_('Only draft or published tenders can be '
                              'cancelled.'))
        self.state = 'cancelled'

    def unlink(self):
        for tender in self:
            if tender.state != 'draft':
                raise UserError(_('A tender that is not a draft cannot be '
                                  'deleted. Audit trail is required.'))
        return super().unlink()

    def _check_tender_deadlines(self):
        today = fields.Date.today()
        tenders = self.search([
            ('state', '=', 'published'),
            ('deadline', '!=', False),
        ])
        for tender in tenders:
            days_left = (tender.deadline.date() - today).days
            if 0 <= days_left <= tender.company_id.sf_tender_alert_days:
                tender.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Tender %s deadline approaching')
                    % (tender.name,),
                    user_id=tender.buyer_id.id)


class TenderCriterion(models.Model):
    _name = 'sf.tender.criterion'
    _description = 'Tender Evaluation Criterion'
    _order = 'tender_id, id'

    tender_id = fields.Many2one('sf.tender', string='Tender', required=True,
                                ondelete='cascade')
    name = fields.Char(string='Criterion', required=True)
    weight = fields.Float(string='Weight (%)', default=25.0, required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('weight_range', 'CHECK(weight >= 0 AND weight <= 100)',
         _('The criterion weight must be between 0 and 100.')),
    ]


class TenderOffer(models.Model):
    _name = 'sf.tender.offer'
    _description = 'Tender Offer'
    _order = 'tender_id, weighted_score desc, id'

    name = fields.Char(string='Number', required=True)
    tender_id = fields.Many2one('sf.tender', string='Tender', required=True,
                                ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string='Supplier',
                                 required=True, ondelete='restrict')
    date_submitted = fields.Datetime(string='Submission date',
                                     default=lambda self:
                                     fields.Datetime.now(),
                                     required=True)
    amount_total = fields.Monetary(string='Total amount',
                                   currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.
                                  currency_id, readonly=True)
    delivery_days = fields.Integer(string='Delivery days')
    eligible = fields.Boolean(string='Administratively compliant',
                              default=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('evaluated', 'Evaluated'),
        ('awarded', 'Awarded'),
        ('rejected', 'Rejected'),
    ], string='Status', default='submitted', required=True)
    score_ids = fields.One2many('sf.tender.offer.score', 'offer_id',
                                string='Scores')
    weighted_score = fields.Float(string='Weighted score', compute='_compute'
                                  '_weighted_score', store=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This offer number already exists.')),
    ]

    @api.depends('score_ids.score', 'score_ids.criterion_id.weight',
                 'score_ids.criterion_id.active')
    def _compute_weighted_score(self):
        for offer in self:
            total_weight = 0.0
            weighted = 0.0
            for score in offer.score_ids:
                if not score.criterion_id.active:
                    continue
                weight = score.criterion_id.weight
                total_weight += weight
                weighted += (score.score / 10.0) * weight
            offer.weighted_score = \
                (weighted / total_weight * 100.0) if total_weight else 0.0

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            tender = self.env['sf.tender'].browse(vals.get('tender_id'))
            seq = self.env['ir.sequence'].next_by_code('sf.tender.offer')
            vals['name'] = 'OFR-%s-%s' % (tender.name, seq)
        return super().create(vals)

    def action_set_evaluated(self):
        self.ensure_one()
        if self.state != 'submitted':
            raise UserError(_('Only submitted offers can be evaluated.'))
        self.state = 'evaluated'

    def _write(self, vals):
        if 'state' in vals and vals.get('state') == 'awarded':
            already_awarded = self.search([
                ('tender_id', '=', self.tender_id.id),
                ('state', '=', 'awarded'),
                ('id', 'not in', self.ids),
            ])
            if already_awarded:
                raise UserError(_('This tender is already awarded to '
                                  'another offer.'))
        return super()._write(vals)


class TenderOfferScore(models.Model):
    _name = 'sf.tender.offer.score'
    _description = 'Tender Offer Score'
    _order = 'offer_id, criterion_id'

    offer_id = fields.Many2one('sf.tender.offer', string='Offer',
                               required=True, ondelete='cascade')
    criterion_id = fields.Many2one('sf.tender.criterion',
                                   string='Criterion', required=True)
    score = fields.Float(string='Score (0-10)', required=True, default=5.0)

    _sql_constraints = [
        ('offer_criterion_uniq', 'UNIQUE(offer_id, criterion_id)',
         _('This criterion is already scored for this offer.')),
        ('score_range', 'CHECK(score >= 0 AND score <= 10)',
         _('The score must be between 0 and 10.')),
    ]


class TenderAwardWizard(models.TransientModel):
    _name = 'sf.tender.award.wizard'
    _description = 'Award Tender'

    tender_id = fields.Many2one('sf.tender', string='Tender',
                                required=True)
    offer_id = fields.Many2one('sf.tender.offer', string='Winning offer',
                               required=True)
    justification = fields.Text(string='Justification')

    @api.onchange('tender_id')
    def _onchange_tender_id(self):
        if self.tender_id:
            return {'domain': {'offer_id': [('tender_id', '=', self.tender_id.id),
                                            ('state', '!=', 'awarded')]}}

    def action_award(self):
        self.ensure_one()
        tender = self.tender_id
        if tender.state != 'in_evaluation':
            raise UserError(_('A tender can be awarded only while it is '
                              'being evaluated.'))
        if not self.justification:
            raise UserError(_('A justification is required to award the '
                              'tender.'))
        offer = self.offer_id
        if offer.tender_id != tender:
            raise UserError(_('The winning offer must belong to this '
                              'tender.'))
        offer.state = 'awarded'
        tender.write({
            'winner_offer_id': offer.id,
            'award_justification': self.justification,
            'award_date': fields.Date.today(),
            'state': 'awarded',
        })
        rejected = tender.offer_ids.filtered(
            lambda o: o.id != offer.id and o.state != 'awarded')
        rejected.write({'state': 'rejected'})
        return {'type': 'ir.actions.act_window_close'}

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.tender'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('deadline', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.deadline
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

