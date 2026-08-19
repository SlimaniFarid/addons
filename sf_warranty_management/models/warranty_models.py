# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Warranty(models.Model):
    _name = 'sf.warranty'
    _description = 'Product Warranty'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    product_tmpl_id = fields.Many2one('product.template',
                                      string='Product', required=True,
                                      ondelete='cascade')
    duration_months = fields.Integer(string='Duration (months)',
                                     required=True)
    coverage = fields.Selection([
        ('parts', 'Parts only'),
        ('parts_labor', 'Parts + Labor'),
        ('full', 'Full coverage'),
    ], string='Coverage', default='full', required=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This warranty number already exists.')),
        ('product_uniq', 'UNIQUE(product_tmpl_id)',
         _('A warranty already exists for this product.')),
        ('duration_positive', 'CHECK(duration_months > 0)',
         _('The warranty duration must be positive.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.warranty')
            vals['name'] = 'WTY-%s' % seq
        return super().create(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_warranty_ids = fields.One2many('sf.warranty', 'product_tmpl_id',
                                      string='Warranties')


class WarrantyClaim(models.Model):
    _name = 'sf.warranty.claim'
    _description = 'Warranty Claim'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    claim_type = fields.Selection([
        ('warranty', 'Warranty'),
        ('goodwill', 'Goodwill'),
    ], string='Type', default='warranty', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, ondelete='restrict',
                                 index=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, ondelete='restrict',
                                 index=True)
    serial_number = fields.Char(string='Serial number')
    invoice_id = fields.Many2one('account.move', string='Sale invoice',
                                 ondelete='restrict')
    purchase_date = fields.Date(string='Purchase date')
    failure_description = fields.Text(string='Failure description',
                                      required=True)
    warranty_id = fields.Many2one('sf.warranty', string='Applicable '
                                  'warranty', compute='_compute_warranty',
                                  store=True)
    eligible = fields.Boolean(string='Eligible')
    eligibility_detail = fields.Text(string='Eligibility detail')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('decision_pending', 'Decision Pending'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    decision = fields.Selection([
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('exception', 'Exception / Goodwill'),
    ], string='Decision')
    decision_reason = fields.Text(string='Decision reason')
    estimated_cost = fields.Monetary(string='Estimated cost',
                                     currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.
                                  currency_id, readonly=True)
    decision_date = fields.Datetime(string='Decision date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This claim number already exists.')),
    ]

    @api.depends('product_id')
    def _compute_warranty(self):
        for claim in self:
            warranty = self.env['sf.warranty'].search([
                ('product_tmpl_id', '=', claim.product_id.product_tmpl_id.id),
                ('active', '=', True),
            ], limit=1)
            claim.warranty_id = warranty.id if warranty else False

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.warranty.claim')
            vals['name'] = 'CLM-%s' % seq
        return super().create(vals)

    def _check_eligibility(self):
        self.ensure_one()
        if not self.product_id or not self.partner_id:
            raise ValidationError(_('A product and a customer are required '
                                    'to check eligibility.'))
        warranty = self.warranty_id
        if not warranty:
            self.eligible = False
            self.eligibility_detail = _('No active warranty is defined for '
                                        'this product.')
            return
        purchase_date = self.purchase_date
        if not purchase_date and self.invoice_id:
            purchase_date = self.invoice_id.invoice_date
        detail = []
        if self.serial_number:
            lot = self.env['stock.lot'].search([
                ('name', '=', self.serial_number),
                ('product_id', '=', self.product_id.id),
            ], limit=1)
            if lot:
                detail.append(_('Serial %s found (%s).') % (
                    self.serial_number, lot.name))
            else:
                detail.append(_('Serial %s not found for this product.')
                              % self.serial_number)
        if not purchase_date:
            self.eligible = False
            detail.append(_('No purchase date available to compute '
                            'coverage.'))
            self.eligibility_detail = ' '.join(detail)
            return
        months = (datetime.now().date() - purchase_date).days / 30.0
        if months <= warranty.duration_months:
            self.eligible = True
            detail.append(_('Purchase %s is within the %s month warranty.')
                          % (purchase_date, warranty.duration_months))
        else:
            self.eligible = False
            detail.append(_('Purchase %s exceeds the %s month warranty.')
                          % (purchase_date, warranty.duration_months))
        self.eligibility_detail = ' '.join(detail)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft claims can be opened.'))
        self.state = 'open'
        if self.company_id.sf_warranty_auto_check:
            self._check_eligibility()
        if not self.eligible:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_('Warranty claim not eligible: %s')
                % (self.name,),
                user_id=self.env.user.id)

    def action_check_eligibility(self):
        self.ensure_one()
        self._check_eligibility()

    def action_open_decision_wizard(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open claims can be decided.'))
        return {
            'name': _('Claim Decision'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.warranty.claim.decision.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_claim_id': self.id},
        }

    def action_cancel(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft claims can be cancelled.'))
        self.state = 'rejected'
        self.decision = 'rejected'
        self.decision_reason = _('Cancelled by operator')

    def unlink(self):
        for claim in self:
            if claim.state in ('open', 'decision_pending'):
                raise UserError(_('A claim being processed cannot be '
                                  'deleted.'))
        return super().unlink()


class WarrantyClaimDecisionWizard(models.TransientModel):
    _name = 'sf.warranty.claim.decision.wizard'
    _description = 'Warranty Claim Decision'

    claim_id = fields.Many2one('sf.warranty.claim', string='Claim',
                               required=True)
    decision = fields.Selection([
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('exception', 'Exception / Goodwill'),
    ], string='Decision', required=True)
    reason = fields.Text(string='Reason')
    estimated_cost = fields.Monetary(string='Estimated cost',
                                     currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.
                                  currency_id, readonly=True)

    @api.onchange('decision')
    def _onchange_decision(self):
        if self.decision != 'rejected':
            self.reason = False

    def action_apply(self):
        self.ensure_one()
        claim = self.claim_id
        if self.decision == 'rejected' and not self.reason:
            raise UserError(_('A reason is required to reject a claim.'))
        claim.write({
            'decision': self.decision,
            'decision_reason': self.reason,
            'decision_date': fields.Datetime.now(),
            'state': 'rejected' if self.decision == 'rejected'
            else 'closed',
            'estimated_cost': self.estimated_cost
            if self.decision != 'rejected' else False,
        })
        return {'type': 'ir.actions.act_window_close'}