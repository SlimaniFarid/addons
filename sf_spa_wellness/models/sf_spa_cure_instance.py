from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import json
from datetime import timedelta


class SpaCureInstance(models.Model):
    _name = 'sf.spa.cure.instance'
    _description = 'Cure Instance'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'
    _sequence_code = 'sf.spa.cure.instance'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    cure_template_id = fields.Many2one('sf.spa.cure.template', string='Cure Template', required=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    state = fields.Selection([
        ('booked', 'Booked'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('interrupted', 'Interrupted'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='booked', tracking=True)
    daily_schedule_ids = fields.One2many('sf.spa.cure.daily.schedule', 'cure_instance_id', string='Daily Schedule')
    total_price = fields.Monetary(string='Total Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    amount_paid = fields.Monetary(string='Amount Paid', default=0.0)
    payment_schedule = fields.Selection([
        ('full', 'Full Payment'),
        ('deposit_30_70', '30% Deposit / 70% Balance'),
        ('monthly', 'Monthly Installments'),
    ], string='Payment Schedule', default='full')
    invoice_ids = fields.One2many('account.move', 'cure_id', string='Invoices')

    @api.depends('start_date', 'cure_template_id.duration_days')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.cure_template_id:
                record.end_date = record.start_date + timedelta(days=record.cure_template_id.duration_days - 1)
            else:
                record.end_date = record.start_date

    def action_book(self):
        for record in self:
            if record.state != 'booked':
                continue
            record._generate_daily_schedule()
            record.state = 'booked'

    def action_start(self):
        for record in self:
            if record.state != 'booked':
                continue
            record.state = 'in_progress'

    def action_complete(self):
        for record in self:
            if record.state != 'in_progress':
                continue
            record.state = 'completed'

    def action_interrupt(self):
        for record in self:
            if record.state != 'in_progress':
                continue
            record.state = 'interrupted'

    def action_cancel(self):
        for record in self:
            if record.state in ('completed', 'cancelled'):
                continue
            record.state = 'cancelled'
            record.daily_schedule_ids.write({'state': 'cancelled'})

    def _generate_daily_schedule(self):
        self.ensure_one()
        self.daily_schedule_ids.unlink()
        template = self.cure_template_id
        daily_data = template.get_daily_schedule()
        
        for day_data in daily_data:
            day_number = day_data.get('day', 1)
            date = self.start_date + timedelta(days=day_number - 1)
            daily_schedule = self.env['sf.spa.cure.daily.schedule'].create({
                'cure_instance_id': self.id,
                'day_number': day_number,
                'date': date,
                'state': 'planned',
            })
            
            for session in day_data.get('sessions', []):
                service_id = session.get('service_id')
                quantity = session.get('quantity', 1)
                preferred_time = session.get('preferred_time')
                
                if not service_id:
                    continue
                
                service = self.env['sf.spa.service'].browse(service_id)
                if not service.exists():
                    continue
                
                for _ in range(quantity):
                    start_dt = fields.Datetime.from_string(f'{date} {preferred_time}') if preferred_time else fields.Datetime.from_string(f'{date} 10:00')
                    self.env['sf.spa.booking'].create({
                        'partner_id': self.partner_id.id,
                        'service_id': service_id,
                        'cure_id': self.id,
                        'start_datetime': start_dt,
                        'state': 'confirmed',
                    })

    def _reschedule_day(self, day_number, new_date=None):
        self.ensure_one()
        daily_schedule = self.daily_schedule_ids.filtered(lambda d: d.day_number == day_number)
        if not daily_schedule:
            return
        if new_date:
            daily_schedule.date = new_date
        daily_schedule.booking_ids.unlink()
        day_data = None
        for d in self.cure_template_id.get_daily_schedule():
            if d.get('day') == day_number:
                day_data = d
                break
        if not day_data:
            return
        for session in day_data.get('sessions', []):
            service_id = session.get('service_id')
            quantity = session.get('quantity', 1)
            preferred_time = session.get('preferred_time')
            if not service_id:
                continue
            service = self.env['sf.spa.service'].browse(service_id)
            if not service.exists():
                continue
            for _ in range(quantity):
                start_dt = fields.Datetime.from_string(f'{daily_schedule.date} {preferred_time}') if preferred_time else fields.Datetime.from_string(f'{daily_schedule.date} 10:00')
                self.env['sf.spa.booking'].create({
                    'partner_id': self.partner_id.id,
                    'service_id': service_id,
                    'cure_id': self.id,
                    'start_datetime': start_dt,
                    'state': 'confirmed',
                })

    @api.constrains('start_date', 'cure_template_id')
    def _check_template(self):
        for record in self:
            if not record.cure_template_id:
                raise ValidationError(_('Cure template is required.'))


class SpaCureDailySchedule(models.Model):
    _name = 'sf.spa.cure.daily.schedule'
    _description = 'Cure Daily Schedule'
    _inherit = ['sf.spa.company.mixin']
    _order = 'day_number'

    cure_instance_id = fields.Many2one('sf.spa.cure.instance', string='Cure Instance', required=True, ondelete='cascade')
    day_number = fields.Integer(string='Day Number', required=True)
    date = fields.Date(string='Date', required=True)
    booking_ids = fields.One2many('sf.spa.booking', 'cure_daily_schedule_id', string='Bookings')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='State', default='planned')
    notes = fields.Text(string='Notes')