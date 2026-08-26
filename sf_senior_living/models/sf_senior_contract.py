from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from .mixin import SfSeniorSequenceMixin, SfSeniorCompanyMixin


class SfSeniorContract(models.Model):
    _name = 'sf.senior.contract'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Stay Contract'
    _order = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, tracking=True, ondelete='cascade')
    residence_id = fields.Many2one('sf.senior.residence', related='resident_id.residence_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    renewal_type = fields.Selection([
        ('automatic', 'Automatic Renewal'),
        ('tacit', 'Tacit Renewal'),
        ('manual', 'Manual Renewal'),
    ], string='Renewal Type', default='tacit', required=True)
    price_accommodation = fields.Monetary(string='Accommodation Price', currency_field='currency_id', required=True)
    price_dependency = fields.Monetary(string='Dependency Price (GIR)', currency_field='currency_id', required=True)
    price_care = fields.Monetary(string='Care Package Price', currency_field='currency_id', required=True)
    price_services = fields.Monetary(string='Services/Activities Price', currency_field='currency_id', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('active', 'Active'),
        ('renewed', 'Renewed'),
        ('terminated', 'Terminated'),
    ], string='Status', default='draft', tracking=True, required=True)
    signed_date = fields.Date(string='Signed Date', tracking=True)
    signed_by_resident = fields.Boolean(string='Signed by Resident/Family', tracking=True)
    signed_by_family = fields.Boolean(string='Signed by Family', tracking=True)
    signed_by_director = fields.Boolean(string='Signed by Director', tracking=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    notes = fields.Html(string='Terms & Conditions')
    document_ids = fields.Many2many('ir.attachment', string='Documents')

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for contract in self:
            if contract.end_date and contract.start_date and contract.end_date < contract.start_date:
                raise ValidationError(_('End date must be after start date.'))

    def action_sign_resident(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can sign contracts.'))
        self.signed_by_resident = True
        self._check_fully_signed()

    def action_sign_family(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can sign contracts.'))
        self.signed_by_family = True
        self._check_fully_signed()

    def action_sign_director(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can sign contracts.'))
        self.signed_by_director = True
        self._check_fully_signed()

    def _check_fully_signed(self):
        for contract in self:
            if contract.signed_by_resident and contract.signed_by_family and contract.signed_by_director:
                contract.state = 'signed'
                contract.signed_date = fields.Date.today()

    def action_activate(self):
        self.ensure_one()
        if self.state != 'signed':
            raise UserError(_('Contract must be signed before activation.'))
        self.state = 'active'
        if self.resident_id.state == 'pre_admission':
            self.resident_id.action_admit()

    def action_renew(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active contracts can be renewed.'))
        new_contract = self.copy({
            'name': '/',
            'start_date': self.end_date or fields.Date.today(),
            'end_date': False,
            'state': 'draft',
            'signed_by_resident': False,
            'signed_by_family': False,
            'signed_by_director': False,
            'signed_date': False,
        })
        self.state = 'renewed'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.senior.contract',
            'res_id': new_contract.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_terminate(self):
        self.ensure_one()
        if self.state not in ('active', 'signed'):
            raise UserError(_('Only active or signed contracts can be terminated.'))
        self.state = 'terminated'
        if self.resident_id.state == 'admitted':
            self.resident_id.action_discharge(reason='other')

    def action_print_contract(self):
        self.ensure_one()
        return self.env.ref('sf_senior_living.action_report_stay_contract').report_action(self)


class SfSeniorCarePlan(models.Model):
    _name = 'sf.senior.care_plan'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Care Plan / PPS'
    _order = 'resident_id, version desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, tracking=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    version = fields.Integer(string='Version', default=1, readonly=True)
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    pps_validated = fields.Boolean(string='PPS Validated', default=False, tracking=True)
    pps_validated_by = fields.Many2one('res.partner', string='Validated By (Physician)', domain="[('is_doctor', '=', True)]", tracking=True)
    pps_validated_date = fields.Date(string='Validation Date', tracking=True)
    objectives = fields.Html(string='Care Objectives')
    nursing_intervention_ids = fields.One2many('sf.senior.nursing_intervention', 'care_plan_id', string='Nursing Interventions')
    prescription_ids = fields.One2many('sf.senior.prescription', 'care_plan_id', string='Prescriptions')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('reviewed', 'Under Review'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True, required=True)
    previous_version_id = fields.Many2one('sf.senior.care_plan', string='Previous Version', copy=False)
    next_version_id = fields.Many2one('sf.senior.care_plan', string='Next Version', copy=False)

    @api.constrains('resident_id', 'state')
    def _check_single_active_care_plan(self):
        for plan in self:
            if plan.state == 'active':
                other = self.search([
                    ('resident_id', '=', plan.resident_id.id),
                    ('state', '=', 'active'),
                    ('id', '!=', plan.id),
                ], limit=1)
                if other:
                    raise ValidationError(_('Resident %s already has an active care plan.') % plan.resident_id.name)

    def action_validate_pps(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_medical'):
            raise UserError(_('Only medical staff can validate PPS.'))
        if not self.prescription_ids:
            raise UserError(_('At least one prescription is required before PPS validation.'))
        if not self.nursing_intervention_ids:
            raise UserError(_('At least one nursing intervention is required before PPS validation.'))
        self.pps_validated = True
        self.pps_validated_by = self.env.user.partner_id
        self.pps_validated_date = fields.Date.today()
        self.state = 'active'
        # Create activity for next review
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=_('PPS Annual Review'),
            note=_('PPS must be reviewed annually'),
            user_id=self.env.user.id,
            date_deadline=fields.Date.add(fields.Date.today(), years=1),
        )

    def action_review(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active care plans can be reviewed.'))
        self.state = 'reviewed'
        # Create new version
        new_version = self.copy({
            'name': '/',
            'version': self.version + 1,
            'start_date': fields.Date.today(),
            'end_date': False,
            'pps_validated': False,
            'pps_validated_by': False,
            'pps_validated_date': False,
            'state': 'draft',
            'previous_version_id': self.id,
        })
        self.next_version_id = new_version
        self.end_date = fields.Date.today()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.senior.care_plan',
            'res_id': new_version.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_archive(self):
        self.ensure_one()
        self.state = 'archived'

    def action_print_pps(self):
        self.ensure_one()
        return self.env.ref('sf_senior_living.action_report_care_plan').report_action(self)


class SfSeniorNursingIntervention(models.Model):
    _name = 'sf.senior.nursing_intervention'
    _inherit = ['sf.senior.company.mixin']
    _description = 'Nursing Intervention'
    _order = 'care_plan_id, intervention_type, frequency'

    name = fields.Char(string='Name', required=True)
    care_plan_id = fields.Many2one('sf.senior.care_plan', string='Care Plan', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    intervention_type = fields.Selection([
        ('hygiene', 'Hygiene & Comfort'),
        ('medical', 'Medical Care'),
        ('monitoring', 'Monitoring & Surveillance'),
        ('mobility', 'Mobility & Transfer'),
        ('nutrition', 'Nutrition & Hydration'),
        ('other', 'Other'),
    ], string='Type', required=True)
    description = fields.Text(string='Description')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('bid', 'Twice Daily (BID)'),
        ('tid', 'Three Times Daily (TID)'),
        ('qid', 'Four Times Daily (QID)'),
        ('weekly', 'Weekly'),
        ('prn', 'As Needed (PRN)'),
    ], string='Frequency', required=True)
    duration_minutes = fields.Integer(string='Duration (minutes)', default=15)
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    assigned_staff_id = fields.Many2one('hr.employee', string='Assigned Staff')
    active = fields.Boolean(default=True)


class SfSeniorPrescription(models.Model):
    _name = 'sf.senior.prescription'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread']
    _description = 'Medical Prescription'
    _order = 'care_plan_id, start_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    care_plan_id = fields.Many2one('sf.senior.care_plan', string='Care Plan', required=True, ondelete='cascade')
    resident_id = fields.Many2one('sf.senior.resident', related='care_plan_id.resident_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    medication_id = fields.Many2one('product.product', string='Medication', required=True, domain="[('is_medication', '=', True)]")
    dosage = fields.Char(string='Dosage', required=True)
    frequency = fields.Char(string='Frequency', required=True)
    route = fields.Selection([
        ('oral', 'Oral'),
        ('subcut', 'Subcutaneous'),
        ('iv', 'Intravenous'),
        ('topical', 'Topical'),
        ('inhalation', 'Inhalation'),
        ('other', 'Other'),
    ], string='Route', required=True, default='oral')
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    prescriber_id = fields.Many2one('res.partner', string='Prescriber', required=True, domain="[('is_doctor', '=', True)]")
    pharmacy_order_id = fields.Many2one('purchase.order', string='Pharmacy Order')
    state = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('stopped', 'Stopped'),
    ], string='Status', default='active', tracking=True, required=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Create pharmacy purchase order if medication is stockable
            if record.medication_id.type in ('product', 'consu') and record.medication_id.qty_available <= 0:
                po = self.env['purchase.order'].create({
                    'partner_id': record.medication_id.seller_ids[:1].partner_id.id or self.env.company.partner_id.id,
                    'order_line': [(0, 0, {
                        'product_id': record.medication_id.id,
                        'name': record.medication_id.name,
                        'product_qty': 1,
                        'price_unit': record.medication_id.standard_price,
                        'date_planned': fields.Date.today(),
                    })],
                })
                record.pharmacy_order_id = po
            # Create activity for medical coordinator
            if record.care_plan_id.resident_id.residence_id.medical_coordinator_id:
                record.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Review new prescription: %s') % record.medication_id.name,
                    note=_('New prescription for resident %s') % record.resident_id.name,
                    user_id=record.care_plan_id.resident_id.residence_id.medical_coordinator_id.user_ids[:1].id or self.env.user.id,
                )
        return records

    def action_stop(self):
        self.ensure_one()
        self.state = 'stopped'
        self.end_date = fields.Date.today()

    def action_suspend(self):
        self.ensure_one()
        self.state = 'suspended'

    def action_reactivate(self):
        self.ensure_one()
        self.state = 'active'