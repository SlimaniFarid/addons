from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MembershipPlan(models.Model):
    _name = 'membership.plan'
    _description = 'Membership Plan'
    _order = 'sequence, name'

    name = fields.Char(string='Plan Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Html(string='Description')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    membership_type = fields.Selection([
        ('individual', 'Individual'),
        ('family', 'Family'),
        ('corporate', 'Corporate'),
        ('student', 'Student'),
    ], string='Type', default='individual', required=True)

    fee = fields.Monetary(string='Annual Fee', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    duration_months = fields.Integer(string='Duration (months)', default=12)
    auto_renew = fields.Boolean(string='Auto Renew', default=True)
    trial_days = fields.Integer(string='Trial Period (days)', default=0)

    max_members = fields.Integer(string='Max Members (0 = unlimited)', default=0)
    benefits = fields.Html(string='Benefits')

    product_id = fields.Many2one('product.product', string='Linked Product', ondelete='set null')
    subscription_ids = fields.One2many('membership.subscription', 'plan_id', string='Subscriptions')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Plan code must be unique.'),
    ]

    @api.constrains('fee')
    def _check_fee(self):
        for r in self:
            if r.fee < 0:
                raise ValidationError('Fee cannot be negative.')

    def action_create_product(self):
        for plan in self:
            if not plan.product_id:
                product = self.env['product.product'].create({
                    'name': f'Membership: {plan.name}',
                    'type': 'service',
                    'list_price': plan.fee,
                    'default_code': f'MEMB-{plan.code}',
                    'categ_id': self.env.ref('product.product_category_all', raise_if_not_found=False).id,
                })
                plan.product_id = product


class MembershipMember(models.Model):
    _name = 'membership.member'
    _description = 'Membership Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='cascade')
    name = fields.Char(related='partner_id.name', store=True, readonly=False)
    email = fields.Char(related='partner_id.email', store=True, readonly=False)
    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    member_code = fields.Char(string='Member Code', required=True, copy=False, default='New')
    member_since = fields.Date(string='Member Since', default=fields.Date.today)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ], string='Status', default='pending', tracking=True)

    subscription_ids = fields.One2many('membership.subscription', 'member_id', string='Subscriptions')
    active_subscription_id = fields.Many2one(
        'membership.subscription', string='Active Subscription',
        compute='_compute_active_subscription', store=True)
    payment_ids = fields.One2many('membership.payment', 'member_id', string='Payments')

    total_paid = fields.Monetary(string='Total Paid', compute='_compute_total_paid', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    notes = fields.Text(string='Internal Notes')

    _sql_constraints = [
        ('member_code_uniq', 'unique(member_code)', 'Member code must be unique.'),
        ('partner_uniq', 'unique(partner_id)', 'A partner can only have one member record.'),
    ]

    @api.depends('subscription_ids.state', 'subscription_ids.end_date')
    def _compute_active_subscription(self):
        for r in self:
            active = r.subscription_ids.filtered(lambda s: s.state in ('active', 'trial'))
            r.active_subscription_id = active.sorted('end_date', reverse=True)[:1] if active else False

    @api.depends('payment_ids.amount', 'payment_ids.state')
    def _compute_total_paid(self):
        for r in self:
            r.total_paid = sum(p.amount for p in r.payment_ids if p.state == 'paid')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('member_code', 'New') == 'New':
                vals['member_code'] = self.env['ir.sequence'].next_by_code('membership.member') or 'MEM-%s' % self.env['ir.sequence'].next_by_code('membership.member')
        return super().create(vals_list)

    def action_activate(self):
        self.status = 'active'
        for sub in self.subscription_ids.filtered(lambda s: s.state == 'pending'):
            sub.action_activate()

    def action_suspend(self):
        self.status = 'suspended'
        self.subscription_ids.filtered(lambda s: s.state == 'active').write({'state': 'suspended'})


class MembershipSubscription(models.Model):
    _name = 'membership.subscription'
    _description = 'Membership Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    member_id = fields.Many2one('membership.member', string='Member', required=True, ondelete='cascade')
    plan_id = fields.Many2one('membership.plan', string='Plan', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Payment'),
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date', required=True)
    auto_renew = fields.Boolean(string='Auto Renew', default=True)

    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    payment_ids = fields.One2many('membership.payment', 'subscription_id', string='Payments')

    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='set null')
    renewal_count = fields.Integer(string='Renewals', default=0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('membership.subscription') or 'SUB-%s' % self.env['ir.sequence'].next_by_code('membership.subscription')
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active' if self.plan_id.trial_days == 0 else 'trial'})

    def action_renew(self):
        for sub in self:
            new_end = sub.end_date + relativedelta(months=sub.plan_id.duration_months)
            new_sub = sub.copy({
                'name': 'New',
                'start_date': sub.end_date + timedelta(days=1),
                'end_date': new_end,
                'state': 'draft',
                'renewal_count': sub.renewal_count + 1,
            })
            sub.auto_renew = False
        return new_sub

    @api.autovacuum
    def _check_expired(self):
        today = fields.Date.today()
        expired = self.search([
            ('state', 'in', ['active', 'trial']),
            ('end_date', '<', today),
        ])
        expired.write({'state': 'expired'})
        expired.mapped('member_id').write({'status': 'expired'})


class MembershipPayment(models.Model):
    _name = 'membership.payment'
    _description = 'Membership Payment'
    _order = 'date desc'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    member_id = fields.Many2one('membership.member', string='Member', required=True, ondelete='cascade')
    subscription_id = fields.Many2one('membership.subscription', string='Subscription', ondelete='set null')
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    date = fields.Date(string='Date', default=fields.Date.today)
    method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit Card'),
        ('online', 'Online'),
        ('other', 'Other'),
    ], string='Method', default='cash')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], string='Status', default='draft', tracking=True)
    reference = fields.Char(string='External Reference')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('membership.payment') or 'PAY-%s' % self.env['ir.sequence'].next_by_code('membership.payment')
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'paid'})
        if self.subscription_id and self.subscription_id.state == 'pending':
            self.subscription_id.action_activate()
        if self.member_id:
            self.member_id.action_activate()

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'membership.plan'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'membership.plan'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
