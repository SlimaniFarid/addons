from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RevRecContract(models.Model):
    _name = 'revrec.contract'
    _description = 'Revenue Recognition Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Contract Reference', required=True, copy=False, default='New')
    sale_order_id = fields.Many2one('sale.order', string='Source Sale Order', ondelete='set null')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda s: s.env.company.currency_id)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    start_date = fields.Date(string='Contract Start', default=fields.Date.today)
    end_date = fields.Date(string='Contract End')
    total_amount = fields.Monetary(string='Total Contract Value', currency_field='currency_id')
    recognized_amount = fields.Monetary(string='Recognized Amount', compute='_compute_recognized', store=True)
    deferred_amount = fields.Monetary(string='Deferred Amount', compute='_compute_recognized', store=True)

    obligation_ids = fields.One2many('revrec.obligation', 'contract_id', string='Performance Obligations')
    schedule_ids = fields.One2many('revrec.schedule', 'contract_id', string='Recognition Schedules')
    allocation_ids = fields.One2many('revrec.allocation', 'contract_id', string='Price Allocations')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('revrec.contract') or 'CONTRACT-%s' % self.env['ir.sequence'].next_by_code('revrec.contract')
        return super().create(vals_list)

    @api.depends('obligation_ids.recognized_amount', 'obligation_ids.allocated_amount')
    def _compute_recognized(self):
        for contract in self:
            contract.recognized_amount = sum(o.recognized_amount for o in contract.obligation_ids)
            total_allocated = sum(o.allocated_amount for o in contract.obligation_ids)
            contract.deferred_amount = total_allocated - contract.recognized_amount

    def action_activate(self):
        self.write({'state': 'active'})
        for obl in self.obligation_ids:
            obl._create_schedules()

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class RevRecObligation(models.Model):
    _name = 'revrec.obligation'
    _description = 'Performance Obligation'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    contract_id = fields.Many2one('revrec.contract', string='Contract', required=True, ondelete='cascade')
    name = fields.Char(string='Obligation Name', required=True)
    description = fields.Text(string='Description')

    obligation_type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service'),
        ('support', 'Support/Maintenance'),
        ('training', 'Training'),
        ('warranty', 'Warranty'),
        ('other', 'Other'),
    ], string='Type', required=True)

    recognition_method = fields.Selection([
        ('point_in_time', 'Point in Time'),
        ('over_time_output', 'Over Time - Output Method'),
        ('over_time_input', 'Over Time - Input Method'),
    ], string='Recognition Method', required=True, default='point_in_time')

    ssp_method = fields.Selection([
        ('observable', 'Observable Price'),
        ('cost_plus', 'Cost Plus Margin'),
        ('residual', 'Residual Approach'),
    ], string='SSP Determination', default='observable')

    allocated_amount = fields.Monetary(string='Allocated Amount', currency_field='currency_id', required=True)
    recognized_amount = fields.Monetary(string='Recognized Amount', compute='_compute_recognized', store=True)
    currency_id = fields.Many2one(related='contract_id.currency_id', store=True)

    product_id = fields.Many2one('product.product', string='Linked Product')
    sale_order_line_id = fields.Many2one('sale.order.line', string='Source Order Line')

    schedule_ids = fields.One2many('revrec.schedule', 'obligation_id', string='Recognition Schedule')

    @api.depends('schedule_ids.recognized_amount')
    def _compute_recognized(self):
        for obl in self:
            obl.recognized_amount = sum(s.recognized_amount for s in obl.schedule_ids if s.state == 'recognized')

    def _create_schedules(self):
        self.ensure_one()
        if self.recognition_method == 'point_in_time':
            self.env['revrec.schedule'].create({
                'obligation_id': self.id,
                'contract_id': self.contract_id.id,
                'planned_date': self.contract_id.start_date,
                'planned_amount': self.allocated_amount,
            })
        else:
            # Over time - create monthly schedules
            from dateutil.relativedelta import relativedelta
            start = self.contract_id.start_date
            end = self.contract_id.end_date or start + relativedelta(months=12)
            months = 1
            current = start
            total_months = 0
            while current < end:
                total_months += 1
                current += relativedelta(months=1)
            monthly_amount = self.allocated_amount / total_months if total_months else 0
            current = start
            while current < end:
                self.env['revrec.schedule'].create({
                    'obligation_id': self.id,
                    'contract_id': self.contract_id.id,
                    'planned_date': current,
                    'planned_amount': monthly_amount,
                })
                current += relativedelta(months=1)


class RevRecSchedule(models.Model):
    _name = 'revrec.schedule'
    _description = 'Revenue Recognition Schedule'
    _order = 'planned_date, id'

    contract_id = fields.Many2one('revrec.contract', string='Contract', required=True, ondelete='cascade')
    obligation_id = fields.Many2one('revrec.obligation', string='Obligation', required=True, ondelete='cascade')
    name = fields.Char(string='Reference', required=True, copy=False, default='New')

    planned_date = fields.Date(string='Planned Date', required=True)
    planned_amount = fields.Monetary(string='Planned Amount', currency_field='currency_id', required=True)
    recognized_amount = fields.Monetary(string='Recognized Amount', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one(related='contract_id.currency_id', store=True)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('recognized', 'Recognized'),
        ('skipped', 'Skipped'),
    ], string='Status', default='pending', tracking=True)

    journal_entry_id = fields.Many2one('account.move', string='Journal Entry', ondelete='set null')
    recognized_date = fields.Date(string='Recognized Date')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('revrec.schedule') or 'SCHED-%s' % self.env['ir.sequence'].next_by_code('revrec.schedule')
        return super().create(vals_list)

    def action_recognize(self):
        for sched in self:
            if sched.state != 'pending':
                continue
            # Create journal entry
            move = self.env['account.move'].create({
                'move_type': 'entry',
                'date': fields.Date.today(),
                'ref': sched.name,
                'line_ids': [
                    (0, 0, {
                        'account_id': sched.obligation_id.contract_id.partner_id.property_account_receivable_id.id,
                        'debit': sched.planned_amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'account_id': sched.obligation_id.contract_id.deferred_account_id.id or False,
                        'debit': 0.0,
                        'credit': sched.planned_amount,
                    }),
                ],
            })
            move.action_post()
            sched.write({
                'state': 'recognized',
                'recognized_amount': sched.planned_amount,
                'recognized_date': fields.Date.today(),
                'journal_entry_id': move.id,
            })

    def action_skip(self):
        self.write({'state': 'skipped'})


class RevRecAllocation(models.Model):
    _name = 'revrec.allocation'
    _description = 'Transaction Price Allocation'

    contract_id = fields.Many2one('revrec.contract', string='Contract', required=True, ondelete='cascade')
    obligation_id = fields.Many2one('revrec.obligation', string='Obligation', required=True)
    ssp_amount = fields.Monetary(string='Standalone Selling Price', currency_field='currency_id')
    allocated_amount = fields.Monetary(string='Allocated Amount', currency_field='currency_id')
    currency_id = fields.Many2one(related='contract_id.currency_id', store=True)
    allocation_method = fields.Selection([
        ('relative_ssp', 'Relative SSP'),
        ('residual', 'Residual'),
        ('observable', 'Observable'),
    ], string='Method', default='relative_ssp')


class RevRecJournal(models.Model):
    _name = 'revrec.journal'
    _description = 'Revenue Recognition Journal Entry'
    _order = 'date desc'

    contract_id = fields.Many2one('revrec.contract', string='Contract', required=True, ondelete='cascade')
    schedule_id = fields.Many2one('revrec.schedule', string='Schedule', ondelete='set null')
    move_id = fields.Many2one('account.move', string='Journal Entry', required=True, ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.today)
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one(related='contract_id.currency_id', store=True)