from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from .mixin import SfSeniorSequenceMixin, SfSeniorCompanyMixin


class SfSeniorResidence(models.Model):
    _name = 'sf.senior.residence'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Senior Residence'
    _order = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    address_id = fields.Many2one('res.partner', string='Address', required=True)
    director_id = fields.Many2one('res.users', string='Director', tracking=True)
    medical_coordinator_id = fields.Many2one('res.partner', string='Medical Coordinator', domain="[('is_doctor', '=', True)]", tracking=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    capacity_total = fields.Integer(string='Total Capacity', default=0)
    active = fields.Boolean(default=True)
    building_ids = fields.One2many('sf.senior.building', 'residence_id', string='Buildings')
    room_ids = fields.One2many('sf.senior.room', 'building_id.residence_id', string='Rooms', readonly=True)
    resident_ids = fields.One2many('sf.senior.resident', 'residence_id', string='Residents')
    contract_ids = fields.One2many('sf.senior.contract', 'resident_id.residence_id', string='Contracts', readonly=True)

    # Configuration fields for billing
    care_fee_monthly = fields.Monetary(string='Monthly Care Fee', currency_field='currency_id', default=0.0)
    service_fee_monthly = fields.Monetary(string='Monthly Service/Activity Fee', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    # Account configuration
    income_account_accommodation_id = fields.Many2one('account.account', string='Accommodation Income Account', domain="[('account_type', '=', 'income')]")
    income_account_dependency_id = fields.Many2one('account.account', string='Dependency Income Account', domain="[('account_type', '=', 'income')]")
    income_account_care_id = fields.Many2one('account.account', string='Care Income Account', domain="[('account_type', '=', 'income')]")
    income_account_service_id = fields.Many2one('account.account', string='Service Income Account', domain="[('account_type', '=', 'income')]")
    income_account_meal_id = fields.Many2one('account.account', string='Meal Income Account', domain="[('account_type', '=', 'income')]")
    journal_id = fields.Many2one('account.journal', string='Default Sales Journal', domain="[('type', '=', 'sale')]")

    # Alert configuration
    gir_alert_days_before = fields.Integer(string='GIR Alert Days Before', default=30)
    gir_alert_days_before_urgent = fields.Integer(string='GIR Urgent Alert Days Before', default=7)
    pps_alert_days_before = fields.Integer(string='PPS Alert Days Before', default=60)
    max_room_reservation_days = fields.Integer(string='Max Room Reservation Days', default=30)
    medical_portal_consent = fields.Boolean(string='Medical Portal Consent Required', default=True)

    # Contract template
    contract_template_id = fields.Many2one('ir.actions.report', string='Contract Template', domain="[('model', '=', 'sf.senior.contract')]")

    @api.depends('building_ids.room_ids')
    def _compute_capacity_total(self):
        for residence in self:
            residence.capacity_total = len(residence.building_ids.room_ids)

    def action_view_rooms(self):
        self.ensure_one()
        return {
            'name': _('Rooms'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.senior.room',
            'view_mode': 'list,form',
            'domain': [('building_id.residence_id', '=', self.id)],
            'context': {'default_residence_id': self.id},
        }

    def action_view_residents(self):
        self.ensure_one()
        return {
            'name': _('Residents'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.senior.resident',
            'view_mode': 'list,form',
            'domain': [('residence_id', '=', self.id)],
            'context': {'default_residence_id': self.id},
        }

    def action_generate_monthly_billing(self):
        self.ensure_one()
        return self.env['sf.senior.billing.wizard'].create({'residence_id': self.id}).action_generate()


class SfSeniorBuilding(models.Model):
    _name = 'sf.senior.building'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread']
    _description = 'Senior Residence Building'
    _order = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    residence_id = fields.Many2one('sf.senior.residence', string='Residence', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    floors = fields.Integer(string='Number of Floors', default=1)
    room_ids = fields.One2many('sf.senior.room', 'building_id', string='Rooms')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_residence_unique', 'unique(name, residence_id)', 'Building reference must be unique per residence!'),
    ]


class SfSeniorRoom(models.Model):
    _name = 'sf.senior.room'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Senior Residence Room'
    _order = 'building_id, floor, name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    building_id = fields.Many2one('sf.senior.building', string='Building', required=True, ondelete='cascade')
    residence_id = fields.Many2one('sf.senior.residence', related='building_id.residence_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    floor = fields.Integer(string='Floor', default=0)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('adapted', 'Adapted (PMR)'),
    ], string='Room Type', required=True, default='single')
    price_accommodation = fields.Monetary(string='Monthly Accommodation Price', currency_field='currency_id', required=True, default=0.0)
    price_dependency_gir1_2 = fields.Monetary(string='Dependency Price GIR 1-2', currency_field='currency_id', default=0.0)
    price_dependency_gir3_4 = fields.Monetary(string='Dependency Price GIR 3-4', currency_field='currency_id', default=0.0)
    price_dependency_gir5_6 = fields.Monetary(string='Dependency Price GIR 5-6', currency_field='currency_id', default=0.0)
    state = fields.Selection([
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
        ('blocked', 'Blocked'),
    ], string='Status', default='free', tracking=True, required=True)
    current_resident_id = fields.Many2one('sf.senior.resident', string='Current Resident', compute='_compute_current_resident', store=True)
    resident_ids = fields.One2many('sf.senior.resident', 'room_id', string='Resident History')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    active = fields.Boolean(default=True)
    surface = fields.Float(string='Surface (m²)')
    notes = fields.Text(string='Notes')

    @api.depends('resident_ids.state', 'resident_id')
    def _compute_current_resident(self):
        for room in self:
            admitted = room.resident_ids.filtered(lambda r: r.state == 'admitted')
            room.current_resident_id = admitted[0] if admitted else False

    @api.constrains('state', 'current_resident_id')
    def _check_room_occupation(self):
        for room in self:
            if room.state == 'occupied' and not room.current_resident_id:
                raise ValidationError(_('An occupied room must have a resident assigned.'))
            if room.current_resident_id and room.current_resident_id.state != 'admitted':
                raise ValidationError(_('Only admitted residents can occupy a room.'))

    @api.onchange('room_type')
    def _onchange_room_type(self):
        if self.room_type == 'adapted':
            self.price_accommodation = self.price_accommodation or 0.0

    def action_set_maintenance(self):
        self.ensure_one()
        if self.state == 'occupied':
            raise UserError(_('Cannot set an occupied room to maintenance. Discharge the resident first.'))
        self.state = 'maintenance'

    def action_set_free(self):
        self.ensure_one()
        if self.state == 'occupied':
            raise UserError(_('Cannot free an occupied room. Discharge the resident first.'))
        self.state = 'free'

    def action_reserve(self, resident_id=None, days=30):
        self.ensure_one()
        if self.state != 'free':
            raise UserError(_('Only free rooms can be reserved.'))
        self.state = 'reserved'
        if resident_id:
            self.env['sf.senior.resident'].browse(resident_id).write({'room_id': self.id, 'state': 'pre_admission'})
        # Schedule activity to convert to admitted or release
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=_('Confirm reservation or release room'),
            note=_('Reservation expires in %d days') % days,
            user_id=self.env.user.id,
            date_deadline=fields.Date.add(fields.Date.today(), days=days),
        )


class SfSeniorResident(models.Model):
    _name = 'sf.senior.resident'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Senior Resident'
    _inherits = {'res.partner': 'partner_id'}
    _order = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade', delegate=True)
    residence_id = fields.Many2one('sf.senior.residence', string='Residence', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    room_id = fields.Many2one('sf.senior.room', string='Room', tracking=True, domain="[('residence_id', '=', residence_id), ('state', 'in', ['free', 'reserved'])]")
    admission_date = fields.Date(string='Admission Date', tracking=True)
    discharge_date = fields.Date(string='Discharge Date', tracking=True)
    discharge_reason = fields.Selection([
        ('transfer', 'Transfer to Another Facility'),
        ('home', 'Return Home'),
        ('deceased', 'Deceased'),
        ('other', 'Other'),
    ], string='Discharge Reason')
    gir_level = fields.Selection([
        ('gir1', 'GIR 1'), ('gir2', 'GIR 2'), ('gir3', 'GIR 3'),
        ('gir4', 'GIR 4'), ('gir5', 'GIR 5'), ('gir6', 'GIR 6'),
    ], string='GIR Level', tracking=True)
    gir_evaluation_date = fields.Date(string='Last GIR Evaluation Date', tracking=True)
    gir_next_evaluation = fields.Date(string='Next GIR Evaluation', compute='_compute_gir_next_evaluation', store=True)
    pps_date = fields.Date(string='PPS Date', tracking=True)
    pps_next_review = fields.Date(string='Next PPS Review', compute='_compute_pps_next_review', store=True)
    contract_id = fields.Many2one('sf.senior.contract', string='Stay Contract')
    state = fields.Selection([
        ('pre_admission', 'Pre-Admission'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('deceased', 'Deceased'),
    ], string='Status', default='pre_admission', tracking=True, required=True)
    family_portal_access = fields.Boolean(string='Family Portal Access', default=True)
    medical_portal_consent = fields.Boolean(string='Medical Data Portal Consent', default=False)

    # Medical info (restricted access)
    pathology_ids = fields.Many2many('sf.senior.pathology', string='Pathologies')
    allergy_ids = fields.Many2many('sf.senior.allergy', string='Allergies')
    treatment_ids = fields.One2many('sf.senior.treatment', 'resident_id', string='Current Treatments')
    care_plan_ids = fields.One2many('sf.senior.care_plan', 'resident_id', string='Care Plans')
    nursing_note_ids = fields.One2many('sf.senior.nursing_note', 'resident_id', string='Nursing Notes')
    gir_evaluation_ids = fields.One2many('sf.senior.gir_evaluation', 'resident_id', string='GIR Evaluations')
    prescription_ids = fields.One2many('sf.senior.prescription', 'care_plan_id.resident_id', string='Prescriptions', readonly=True)
    activity_participant_ids = fields.Many2many('sf.senior.activity', 'sf_senior_activity_resident_rel', string='Activities')
    meal_regime_ids = fields.One2many('sf.senior.meal_regime', 'resident_id', string='Meal Regimes')
    meal_order_ids = fields.One2many('sf.senior.meal_order', 'resident_id', string='Meal Orders')
    invoice_line_ids = fields.One2many('sf.senior.invoice_line', 'resident_id', string='Invoice Lines')
    family_message_ids = fields.One2many('sf.senior.family_message', 'resident_id', string='Family Messages')

    # Family contacts
    family_contact_ids = fields.One2many('sf.senior.family_contact', 'resident_id', string='Family Contacts')
    tutor_id = fields.Many2one('res.partner', string='Legal Tutor', domain="[('is_company', '=', False)]")
    emergency_contact_id = fields.Many2one('res.partner', string='Emergency Contact', domain="[('is_company', '=', False)]")

    @api.depends('gir_evaluation_date')
    def _compute_gir_next_evaluation(self):
        for resident in self:
            if resident.gir_evaluation_date:
                resident.gir_next_evaluation = fields.Date.add(resident.gir_evaluation_date, months=6)
            elif resident.admission_date:
                resident.gir_next_evaluation = fields.Date.add(resident.admission_date, months=6)
            else:
                resident.gir_next_evaluation = False

    @api.depends('pps_date')
    def _compute_pps_next_review(self):
        for resident in self:
            if resident.pps_date:
                resident.pps_next_review = fields.Date.add(resident.pps_date, years=1)
            else:
                resident.pps_next_review = False

    @api.constrains('room_id', 'state')
    def _check_room_unique_occupation(self):
        for resident in self:
            if resident.room_id and resident.state == 'admitted':
                other = self.search([
                    ('room_id', '=', resident.room_id.id),
                    ('state', '=', 'admitted'),
                    ('id', '!=', resident.id),
                ], limit=1)
                if other:
                    raise ValidationError(_('Room %s is already occupied by %s') % (resident.room_id.name, other.name))

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'admitted' and not self.admission_date:
            self.admission_date = fields.Date.today()
        elif self.state in ('discharged', 'deceased') and not self.discharge_date:
            self.discharge_date = fields.Date.today()
        if self.state == 'admitted' and self.room_id:
            self.room_id.state = 'occupied'
        elif self.state in ('discharged', 'deceased') and self.room_id:
            # Check if other admitted residents in same room
            other = self.search([('room_id', '=', self.room_id.id), ('state', '=', 'admitted'), ('id', '!=', self.id)], limit=1)
            if not other:
                self.room_id.state = 'free'

    def action_admit(self):
        self.ensure_one()
        if not self.room_id:
            raise UserError(_('A room must be assigned before admission.'))
        if self.room_id.state not in ('free', 'reserved'):
            raise UserError(_('Room %s is not available for admission.') % self.room_id.name)
        if not self.contract_id or self.contract_id.state != 'active':
            raise UserError(_('An active stay contract is required for admission.'))
        self.state = 'admitted'
        self.room_id.state = 'occupied'
        self.admission_date = fields.Date.today()
        # Create initial care plan
        self.env['sf.senior.care_plan'].create({
            'resident_id': self.id,
            'start_date': fields.Date.today(),
            'state': 'draft',
        })
        # Schedule GIR evaluation if not done
        if not self.gir_evaluation_date:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_('Perform initial GIR evaluation'),
                user_id=self.env.user.id,
                date_deadline=fields.Date.add(fields.Date.today(), days=30),
            )

    def action_discharge(self, reason='transfer'):
        self.ensure_one()
        if self.state != 'admitted':
            raise UserError(_('Only admitted residents can be discharged.'))
        self.state = 'discharged'
        self.discharge_reason = reason
        self.discharge_date = fields.Date.today()
        if self.room_id:
            other = self.search([('room_id', '=', self.room_id.id), ('state', '=', 'admitted'), ('id', '!=', self.id)], limit=1)
            if not other:
                self.room_id.state = 'free'
        # Close contract
        if self.contract_id and self.contract_id.state == 'active':
            self.contract_id.state = 'terminated'

    def action_deceased(self):
        self.ensure_one()
        self.action_discharge(reason='deceased')
        self.state = 'deceased'

    def action_pre_admission(self):
        self.ensure_one()
        self.state = 'pre_admission'

    def _get_dependency_price(self):
        self.ensure_one()
        if not self.room_id:
            return 0.0
        gir_map = {
            'gir1': self.room_id.price_dependency_gir1_2,
            'gir2': self.room_id.price_dependency_gir1_2,
            'gir3': self.room_id.price_dependency_gir3_4,
            'gir4': self.room_id.price_dependency_gir3_4,
            'gir5': self.room_id.price_dependency_gir5_6,
            'gir6': self.room_id.price_dependency_gir5_6,
        }
        return gir_map.get(self.gir_level, 0.0)


class SfSeniorFamilyContact(models.Model):
    _name = 'sf.senior.family_contact'
    _description = 'Resident Family Contact'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)
    relationship = fields.Selection([
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('grandchild', 'Grandchild'),
        ('sibling', 'Sibling'),
        ('nephew_niece', 'Nephew/Niece'),
        ('friend', 'Friend'),
        ('legal', 'Legal Representative'),
        ('other', 'Other'),
    ], string='Relationship', required=True)
    is_main_contact = fields.Boolean(string='Main Contact')
    has_portal_access = fields.Boolean(string='Portal Access', default=True)
    sequence = fields.Integer(default=10)
    phone = fields.Char(related='partner_id.phone')
    email = fields.Char(related='partner_id.email')


class SfSeniorPathology(models.Model):
    _name = 'sf.senior.pathology'
    _description = 'Pathology'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code (ICD-10)')
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)


class SfSeniorAllergy(models.Model):
    _name = 'sf.senior.allergy'
    _description = 'Allergy'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    allergen_type = fields.Selection([
        ('medication', 'Medication'),
        ('food', 'Food'),
        ('environmental', 'Environmental'),
        ('other', 'Other'),
    ], string='Allergen Type', required=True)
    severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('anaphylactic', 'Anaphylactic'),
    ], string='Severity', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)


class SfSeniorTreatment(models.Model):
    _name = 'sf.senior.treatment'
    _description = 'Current Treatment'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, ondelete='cascade')
    medication_id = fields.Many2one('product.product', string='Medication', domain="[('is_medication', '=', True)]")
    dosage = fields.Char(string='Dosage')
    frequency = fields.Char(string='Frequency')
    route = fields.Selection([
        ('oral', 'Oral'),
        ('subcut', 'Subcutaneous'),
        ('iv', 'Intravenous'),
        ('topical', 'Topical'),
        ('inhalation', 'Inhalation'),
        ('other', 'Other'),
    ], string='Route')
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    prescriber_id = fields.Many2one('res.partner', string='Prescriber', domain="[('is_doctor', '=', True)]")
    active = fields.Boolean(default=True)