from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import calendar


class SfSeniorBillingWizard(models.TransientModel):
    _name = 'sf.senior.billing.wizard'
    _description = 'Monthly Billing Generation Wizard'

    residence_id = fields.Many2one('sf.senior.residence', string='Residence', required=True)
    period_start = fields.Date(string='Period Start', required=True, default=lambda self: fields.Date.today().replace(day=1))
    period_end = fields.Date(string='Period End', required=True, default=lambda self: (fields.Date.today().replace(day=1) + relativedelta(months=1, days=-1)))
    generate_accommodation = fields.Boolean(string='Accommodation', default=True)
    generate_dependency = fields.Boolean(string='Dependency (GIR)', default=True)
    generate_care = fields.Boolean(string='Care Package', default=True)
    generate_services = fields.Boolean(string='Services/Activities', default=True)
    generate_meals = fields.Boolean(string='Meals', default=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today)
    due_date = fields.Date(string='Due Date', default=lambda self: fields.Date.today() + relativedelta(days=30))

    def action_generate(self):
        self.ensure_one()
        residents = self.env['sf.senior.resident'].search([
            ('residence_id', '=', self.residence_id.id),
            ('state', '=', 'admitted'),
        ])

        if not residents:
            raise UserError(_('No admitted residents found for this residence.'))

        # Create invoice per resident
        invoices = self.env['account.move']
        for resident in residents:
            invoice = self._create_resident_invoice(resident)
            invoices |= invoice

        # Post invoices
        invoices.action_post()

        return {
            'name': _('Generated Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoices.ids)],
            'context': {'create': False},
        }

    def _create_resident_invoice(self, resident):
        # Calculate days in period
        days_in_month = calendar.monthrange(self.period_start.year, self.period_start.month)[1]
        admission_date = resident.admission_date or self.period_start
        discharge_date = resident.discharge_date or self.period_end
        
        # Days present in period
        period_start = max(self.period_start, admission_date)
        period_end = min(self.period_end, discharge_date)
        if period_start > period_end:
            return False
        days_present = (period_end - period_start).days + 1
        prorata = days_present / days_in_month if days_in_month > 0 else 0

        # Create invoice
        partner = resident.partner_id.commercial_partner_id
        journal = self.residence_id.journal_id or self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': self.invoice_date,
            'invoice_date_due': self.due_date,
            'journal_id': journal.id,
            'currency_id': self.residence_id.currency_id.id,
            'company_id': self.residence_id.company_id.id,
            'ref': _('Monthly billing %s - %s') % (resident.name, self.period_start.strftime('%m/%Y')),
        }
        invoice = self.env['account.move'].create(invoice_vals)

        lines = []

        # 1. Accommodation
        if self.generate_accommodation and resident.room_id:
            price = resident.room_id.price_accommodation * prorata
            lines.append((0, 0, {
                'name': _('Accommodation - %s (%d days)') % (resident.room_id.name, days_present),
                'account_id': self.residence_id.income_account_accommodation_id.id or journal.default_account_id.id,
                'quantity': 1,
                'price_unit': price,
                'tax_ids': [(6, 0, journal.default_tax_ids.ids)],
            }))
            # Create invoice line record
            self.env['sf.senior.invoice_line'].create({
                'resident_id': resident.id,
                'invoice_id': invoice.id,
                'period_start': self.period_start,
                'period_end': self.period_end,
                'line_type': 'accommodation',
                'description': _('Accommodation - %s') % resident.room_id.name,
                'quantity': 1,
                'price_unit': price,
                'gir_level_at_billing': resident.gir_level,
            })

        # 2. Dependency (GIR)
        if self.generate_dependency and resident.gir_level:
            dependency_price = resident._get_dependency_price() * prorata
            lines.append((0, 0, {
                'name': _('Dependency - %s (%d days)') % (dict(resident._fields['gir_level'].selection).get(resident.gir_level), days_present),
                'account_id': self.residence_id.income_account_dependency_id.id or journal.default_account_id.id,
                'quantity': 1,
                'price_unit': dependency_price,
                'tax_ids': [(6, 0, journal.default_tax_ids.ids)],
            }))
            self.env['sf.senior.invoice_line'].create({
                'resident_id': resident.id,
                'invoice_id': invoice.id,
                'period_start': self.period_start,
                'period_end': self.period_end,
                'line_type': 'dependency',
                'description': _('Dependency - %s') % dict(resident._fields['gir_level'].selection).get(resident.gir_level),
                'quantity': 1,
                'price_unit': dependency_price,
                'gir_level_at_billing': resident.gir_level,
            })

        # 3. Care Package
        if self.generate_care:
            care_price = self.residence_id.care_fee_monthly * prorata
            lines.append((0, 0, {
                'name': _('Care Package (%d days)') % days_present,
                'account_id': self.residence_id.income_account_care_id.id or journal.default_account_id.id,
                'quantity': 1,
                'price_unit': care_price,
                'tax_ids': [(6, 0, journal.default_tax_ids.ids)],
            }))
            self.env['sf.senior.invoice_line'].create({
                'resident_id': resident.id,
                'invoice_id': invoice.id,
                'period_start': self.period_start,
                'period_end': self.period_end,
                'line_type': 'care',
                'description': _('Care Package'),
                'quantity': 1,
                'price_unit': care_price,
                'gir_level_at_billing': resident.gir_level,
            })

        # 4. Services/Activities
        if self.generate_services:
            service_price = self.residence_id.service_fee_monthly * prorata
            lines.append((0, 0, {
                'name': _('Services & Activities (%d days)') % days_present,
                'account_id': self.residence_id.income_account_service_id.id or journal.default_account_id.id,
                'quantity': 1,
                'price_unit': service_price,
                'tax_ids': [(6, 0, journal.default_tax_ids.ids)],
            }))
            self.env['sf.senior.invoice_line'].create({
                'resident_id': resident.id,
                'invoice_id': invoice.id,
                'period_start': self.period_start,
                'period_end': self.period_end,
                'line_type': 'services',
                'description': _('Services & Activities'),
                'quantity': 1,
                'price_unit': service_price,
                'gir_level_at_billing': resident.gir_level,
            })

        # 5. Meals (served meals in period)
        if self.generate_meals:
            meal_orders = self.env['sf.senior.meal_order'].search([
                ('resident_id', '=', resident.id),
                ('state', '=', 'served'),
                ('served_date', '>=', self.period_start),
                ('served_date', '<=', self.period_end),
                ('billed', '=', False),
            ])
            if meal_orders:
                total_meals = sum(meal_orders.mapped('quantity'))
                total_price = sum(meal_orders.mapped('price'))
                lines.append((0, 0, {
                    'name': _('Meals (%d meals)') % total_meals,
                    'account_id': self.residence_id.income_account_meal_id.id or journal.default_account_id.id,
                    'quantity': 1,
                    'price_unit': total_price,
                    'tax_ids': [(6, 0, journal.default_tax_ids.ids)],
                }))
                self.env['sf.senior.invoice_line'].create({
                    'resident_id': resident.id,
                    'invoice_id': invoice.id,
                    'period_start': self.period_start,
                    'period_end': self.period_end,
                    'line_type': 'meals',
                    'description': _('Meals (%d meals)') % total_meals,
                    'quantity': 1,
                    'price_unit': total_price,
                    'gir_level_at_billing': resident.gir_level,
                })
                # Mark as billed
                meal_orders.write({'billed': True})

        if lines:
            invoice.write({'invoice_line_ids': lines})
        
        return invoice


class SfSeniorBillingCron(models.Model):
    _name = 'sf.senior.billing.cron'
    _description = 'Monthly Billing Cron'

    @api.model
    def _cron_generate_monthly_billing(self):
        """Cron job to generate monthly billing for all residences"""
        today = fields.Date.today()
        # Run on 1st of each month for previous month
        period_start = (today.replace(day=1) - relativedelta(months=1))
        period_end = today.replace(day=1) - relativedelta(days=1)
        
        residences = self.env['sf.senior.residence'].search([('active', '=', True)])
        for residence in residences:
            try:
                wizard = self.env['sf.senior.billing.wizard'].create({
                    'residence_id': residence.id,
                    'period_start': period_start,
                    'period_end': period_end,
                })
                wizard.action_generate()
            except Exception as e:
                # Log error but continue with other residences
                self.env['ir.logging'].create({
                    'name': 'Senior Living Billing Cron',
                    'type': 'error',
                    'dbname': self._cr.dbname,
                    'message': _('Failed to generate billing for residence %s: %s') % (residence.name, str(e)),
                })


class SfSeniorAlertCron(models.Model):
    _name = 'sf.senior.alert.cron'
    _description = 'Alert Generation Cron'

    @api.model
    def _cron_check_gir_evaluations(self):
        """Check for upcoming GIR evaluations and create alerts"""
        today = fields.Date.today()
        config = self.env['ir.config_parameter'].sudo()
        alert_days = int(config.get_param('sf_senior_living.gir_alert_days', 30))
        urgent_days = int(config.get_param('sf_senior_living.gir_alert_days_urgent', 7))

        # Find residents with GIR evaluation due
        residents = self.env['sf.senior.resident'].search([
            ('state', '=', 'admitted'),
            ('gir_next_evaluation', '!=', False),
        ])

        for resident in residents:
            days_until = (resident.gir_next_evaluation - today).days
            if days_until in (alert_days, urgent_days):
                priority = 'urgent' if days_until <= urgent_days else 'high'
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('GIR Evaluation Due for %s') % resident.name,
                    'note': _('GIR evaluation is due in %d days (by %s)') % (days_until, resident.gir_next_evaluation),
                    'user_id': resident.residence_id.medical_coordinator_id.user_ids[:1].id or self.env.user.id,
                    'res_id': resident.id,
                    'res_model_id': self.env['ir.model']._get('sf.senior.resident').id,
                    'date_deadline': resident.gir_next_evaluation,
                })

    @api.model
    def _cron_check_pps_reviews(self):
        """Check for upcoming PPS reviews"""
        today = fields.Date.today()
        config = self.env['ir.config_parameter'].sudo()
        alert_days = int(config.get_param('sf_senior_living.pps_alert_days', 60))

        residents = self.env['sf.senior.resident'].search([
            ('state', '=', 'admitted'),
            ('pps_next_review', '!=', False),
        ])

        for resident in residents:
            days_until = (resident.pps_next_review - today).days
            if days_until == alert_days:
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('PPS Review Due for %s') % resident.name,
                    'note': _('PPS (Personalized Care Plan) review is due in %d days (by %s)') % (alert_days, resident.pps_next_review),
                    'user_id': resident.residence_id.medical_coordinator_id.user_ids[:1].id or self.env.user.id,
                    'res_id': resident.id,
                    'res_model_id': self.env['ir.model']._get('sf.senior.resident').id,
                    'date_deadline': resident.pps_next_review,
                })

    @api.model
    def _cron_check_contract_renewals(self):
        """Check for upcoming contract renewals"""
        today = fields.Date.today()
        alert_days = 30

        contracts = self.env['sf.senior.contract'].search([
            ('state', '=', 'active'),
            ('end_date', '!=', False),
            ('renewal_type', '!=', 'manual'),
        ])

        for contract in contracts:
            days_until = (contract.end_date - today).days
            if days_until == alert_days:
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('Contract Renewal for %s') % contract.resident_id.name,
                    'note': _('Stay contract expires in %d days (on %s). Renewal type: %s') % (days_until, contract.end_date, contract.renewal_type),
                    'user_id': contract.resident_id.residence_id.director_id.id or self.env.user.id,
                    'res_id': contract.id,
                    'res_model_id': self.env['ir.model']._get('sf.senior.contract').id,
                    'date_deadline': contract.end_date,
                })

    @api.model
    def _cron_check_birthdays(self):
        """Check for resident birthdays"""
        today = fields.Date.today()
        residents = self.env['sf.senior.resident'].search([
            ('state', '=', 'admitted'),
        ])

        for resident in residents:
            if resident.partner_id.birthdate:
                bday_this_year = resident.partner_id.birthdate.replace(year=today.year)
                days_until = (bday_this_year - today).days
                if days_until == 7:  # Alert 1 week before
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': _('Birthday: %s') % resident.name,
                        'note': _('%s will celebrate their birthday on %s') % (resident.name, bday_this_year),
                        'user_id': resident.residence_id.director_id.id or self.env.user.id,
                        'res_id': resident.id,
                        'res_model_id': self.env['ir.model']._get('sf.senior.resident').id,
                        'date_deadline': bday_this_year,
                    })