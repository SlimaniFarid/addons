from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from .mixin import SfSeniorSequenceMixin, SfSeniorCompanyMixin


class SfSeniorNursingNote(models.Model):
    _name = 'sf.senior.nursing_note'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread']
    _description = 'Nursing Note / Handover'
    _order = 'note_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, tracking=True, ondelete='cascade')
    care_plan_id = fields.Many2one('sf.senior.care_plan', string='Care Plan')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    author_id = fields.Many2one('hr.employee', string='Author', required=True, default=lambda self: self.env.user.employee_id)
    note_date = fields.Datetime(string='Date/Time', required=True, default=fields.Datetime.now, tracking=True)
    shift = fields.Selection([
        ('morning', 'Morning (6h-14h)'),
        ('afternoon', 'Afternoon (14h-22h)'),
        ('night', 'Night (22h-6h)'),
    ], string='Shift', required=True)
    content = fields.Html(string='Content', required=True)
    alert = fields.Boolean(string='Alert', default=False, tracking=True)
    alert_type = fields.Selection([
        ('medical', 'Medical'),
        ('behavioral', 'Behavioral'),
        ('fall', 'Fall'),
        ('pain', 'Pain'),
        ('other', 'Other'),
    ], string='Alert Type')
    intervention_ids = fields.Many2many('sf.senior.nursing_intervention', string='Related Interventions')
    read_by_ids = fields.Many2many('hr.employee', string='Read By')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.alert:
                # Notify medical coordinator and care team
                residence = record.resident_id.residence_id
                if residence.medical_coordinator_id:
                    record.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('ALERT: %s - %s') % (record.alert_type, record.resident_id.name),
                        note=record.content,
                        user_id=residence.medical_coordinator_id.user_ids[:1].id or self.env.user.id,
                        date_deadline=fields.Date.today(),
                    )
                # Also notify care plan responsible
                if record.care_plan_id:
                    for intervention in record.care_plan_id.nursing_intervention_ids:
                        if intervention.assigned_staff_id and intervention.assigned_staff_id.user_id:
                            record.activity_schedule(
                                'mail.mail_activity_data_todo',
                                summary=_('ALERT on intervention: %s') % intervention.name,
                                note=record.content,
                                user_id=intervention.assigned_staff_id.user_id.id,
                                date_deadline=fields.Date.today(),
                            )
        return records

    def action_mark_read(self):
        self.ensure_one()
        self.read_by_ids = [(4, self.env.user.employee_id.id)] if self.env.user.employee_id else []


class SfSeniorGirEvaluation(models.Model):
    _name = 'sf.senior.gir_evaluation'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'GIR/AGGIR Evaluation'
    _order = 'evaluation_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, tracking=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    evaluator_id = fields.Many2one('hr.employee', string='Evaluator', required=True, tracking=True)
    evaluation_date = fields.Date(string='Evaluation Date', required=True, tracking=True, default=fields.Date.today)
    gir_level = fields.Selection([
        ('gir1', 'GIR 1'), ('gir2', 'GIR 2'), ('gir3', 'GIR 3'),
        ('gir4', 'GIR 4'), ('gir5', 'GIR 5'), ('gir6', 'GIR 6'),
    ], string='GIR Level', required=True, tracking=True)
    score_total = fields.Integer(string='Total Score', compute='_compute_score_total', store=True)
    details = fields.Json(string='AGGIR Details (10 variables)')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('validated', 'Validated'),
        ('locked', 'Locked'),
    ], string='Status', default='scheduled', tracking=True, required=True)
    validated_by = fields.Many2one('hr.employee', string='Validated By', tracking=True)
    validated_date = fields.Date(string='Validation Date', tracking=True)
    notes = fields.Text(string='Notes')

    # AGGIR 10 variables
    coherence = fields.Integer(string='Coherence', default=0)
    orientation = fields.Integer(string='Orientation', default=0)
    toilette = fields.Integer(string='Toilette', default=0)
    habillage = fields.Integer(string='Habillage', default=0)
    alimentation = fields.Integer(string='Alimentation', default=0)
    elimination = fields.Integer(string='Elimination', default=0)
    transfert = fields.Integer(string='Transfert', default=0)
    deplacement_int = fields.Integer(string='Déplacement Intérieur', default=0)
    deplacement_ext = fields.Integer(string='Déplacement Extérieur', default=0)
    communication = fields.Integer(string='Communication', default=0)

    @api.depends('coherence', 'orientation', 'toilette', 'habillage', 'alimentation',
                 'elimination', 'transfert', 'deplacement_int', 'deplacement_ext', 'communication')
    def _compute_score_total(self):
        for eval in self:
            eval.score_total = sum([
                eval.coherence, eval.orientation, eval.toilette, eval.habillage,
                eval.alimentation, eval.elimination, eval.transfert,
                eval.deplacement_int, eval.deplacement_ext, eval.communication
            ])

    @api.onchange('score_total')
    def _onchange_score_total(self):
        for eval in self:
            if eval.score_total <= 6:
                eval.gir_level = 'gir1'
            elif eval.score_total <= 11:
                eval.gir_level = 'gir2'
            elif eval.score_total <= 16:
                eval.gir_level = 'gir3'
            elif eval.score_total <= 21:
                eval.gir_level = 'gir4'
            elif eval.score_total <= 26:
                eval.gir_level = 'gir5'
            else:
                eval.gir_level = 'gir6'

    def action_start_evaluation(self):
        self.ensure_one()
        if self.state != 'scheduled':
            raise UserError(_('Only scheduled evaluations can be started.'))
        self.state = 'in_progress'

    def action_validate(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can validate GIR evaluations.'))
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress evaluations can be validated.'))
        self.state = 'validated'
        self.validated_by = self.env.user.employee_id
        self.validated_date = fields.Date.today()
        # Update resident GIR level
        self.resident_id.gir_level = self.gir_level
        self.resident_id.gir_evaluation_date = self.evaluation_date
        # Schedule next evaluation
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=_('Next GIR Evaluation for %s') % self.resident_id.name,
            note=_('GIR evaluation due in 6 months'),
            user_id=self.evaluator_id.user_id.id or self.env.user.id,
            date_deadline=fields.Date.add(self.evaluation_date, months=6),
        )

    def action_lock(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can lock GIR evaluations.'))
        if self.state != 'validated':
            raise UserError(_('Only validated evaluations can be locked.'))
        self.state = 'locked'

    def action_unlock(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Only managers can unlock GIR evaluations.'))
        self.state = 'validated'

    def write(self, vals):
        if self.state == 'locked' and not self.env.user.has_group('sf_senior_living.group_sf_senior_manager'):
            raise UserError(_('Locked GIR evaluations cannot be modified.'))
        return super().write(vals)

    def action_print_gir(self):
        self.ensure_one()
        return self.env.ref('sf_senior_living.action_report_gir_evaluation').report_action(self)


class SfSeniorActivity(models.Model):
    _name = 'sf.senior.activity'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Activity / Entertainment'
    _order = 'planned_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    residence_id = fields.Many2one('sf.senior.residence', string='Residence', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    activity_type = fields.Selection([
        ('physical', 'Physical'),
        ('cognitive', 'Cognitive'),
        ('social', 'Social'),
        ('creative', 'Creative'),
        ('therapeutic', 'Therapeutic'),
        ('outdoor', 'Outdoor'),
        ('cultural', 'Cultural'),
    ], string='Type', required=True)
    category = fields.Selection([
        ('individual', 'Individual'),
        ('group', 'Group'),
    ], string='Category', required=True, default='group')
    description = fields.Html(string='Description')
    location_id = fields.Many2one('sf.senior.room', string='Location', domain="[('residence_id', '=', residence_id), ('room_type', '!=', 'adapted')]")
    animator_id = fields.Many2one('hr.employee', string='Animator', tracking=True)
    planned_date = fields.Datetime(string='Planned Date', required=True, tracking=True)
    duration_minutes = fields.Integer(string='Duration (minutes)', default=60)
    capacity_max = fields.Integer(string='Max Capacity', default=10)
    state = fields.Selection([
        ('planned', 'Planned'),
        ('open_registration', 'Open for Registration'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', tracking=True, required=True)
    participant_ids = fields.Many2many('sf.senior.resident', 'sf_senior_activity_resident_rel', string='Participants')
    waitlist_ids = fields.Many2many('sf.senior.resident', 'sf_senior_activity_waitlist_rel', string='Waitlist')
    actual_participants = fields.Integer(string='Actual Participants', compute='_compute_actual_participants')
    notes = fields.Text(string='Notes')

    @api.depends('participant_ids')
    def _compute_actual_participants(self):
        for act in self:
            act.actual_participants = len(act.participant_ids)

    def action_open_registration(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned activities can be opened for registration.'))
        self.state = 'open_registration'

    def action_start(self):
        self.ensure_one()
        if self.state not in ('planned', 'open_registration'):
            raise UserError(_('Activity must be planned or open for registration to start.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress activities can be marked as done.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('Completed activities cannot be cancelled.'))
        self.state = 'cancelled'
        # Notify participants
        for participant in self.participant_ids:
            self.env['sf.senior.family_message'].create({
                'resident_id': participant.id,
                'sender_id': self.env.user.id,
                'recipient_type': 'family',
                'subject': _('Activity Cancelled: %s') % self.name,
                'body': _('The activity "%s" scheduled for %s has been cancelled.') % (self.name, self.planned_date),
                'priority': 'high',
            })

    def action_register_participant(self, resident_id):
        self.ensure_one()
        if self.state != 'open_registration':
            raise UserError(_('Registration is not open for this activity.'))
        if len(self.participant_ids) >= self.capacity_max:
            # Add to waitlist
            self.waitlist_ids = [(4, resident_id)]
            return {'waitlisted': True}
        self.participant_ids = [(4, resident_id)]
        return {'waitlisted': False}

    def action_unregister_participant(self, resident_id):
        self.ensure_one()
        self.participant_ids = [(3, resident_id)]
        # Promote from waitlist
        if self.waitlist_ids:
            next_resident = self.waitlist_ids[0]
            self.waitlist_ids = [(3, next_resident.id)]
            self.participant_ids = [(4, next_resident.id)]
            # Notify
            self.env['sf.senior.family_message'].create({
                'resident_id': next_resident.id,
                'sender_id': self.env.user.id,
                'recipient_type': 'family',
                'subject': _('Waitlist Promotion: %s') % self.name,
                'body': _('A spot opened up for the activity "%s". You have been registered.') % self.name,
                'priority': 'normal',
            })


class SfSeniorMealRegime(models.Model):
    _name = 'sf.senior.meal_regime'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin']
    _description = 'Meal Regime / Dietary Regime'
    _order = 'resident_id, start_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    regime_type = fields.Selection([
        ('normal', 'Normal'),
        ('diabetic', 'Diabetic'),
        ('low_salt', 'Low Salt'),
        ('blended', 'Blended/Mixed'),
        ('chopped', 'Chopped'),
        ('high_protein', 'High Protein'),
        ('renal', 'Renal'),
        ('custom', 'Custom'),
    ], string='Regime Type', required=True, default='normal')
    description = fields.Text(string='Description / Details')
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    prescriber_id = fields.Many2one('res.partner', string='Prescriber', domain="[('is_doctor', '=', True)]")
    active = fields.Boolean(default=True)


class SfSeniorMenu(models.Model):
    _name = 'sf.senior.menu'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin']
    _description = 'Menu'
    _order = 'date desc, meal_type'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    residence_id = fields.Many2one('sf.senior.residence', string='Residence', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    date = fields.Date(string='Date', required=True)
    meal_type = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
    ], string='Meal Type', required=True)
    dishes = fields.Html(string='Dishes')
    regime_variants = fields.Json(string='Regime Variants', help='Mapping of regime_type to adapted dish')
    meal_order_ids = fields.One2many('sf.senior.meal_order', 'menu_id', string='Orders')

    _sql_constraints = [
        ('unique_menu', 'unique(residence_id, date, meal_type)', 'A menu for this residence, date and meal type already exists!'),
    ]


class SfSeniorMealOrder(models.Model):
    _name = 'sf.senior.meal_order'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin']
    _description = 'Meal Order'
    _order = 'menu_id, resident_id'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', ondelete='set null')
    menu_id = fields.Many2one('sf.senior.menu', string='Menu', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    meal_type = fields.Selection(related='menu_id.meal_type', store=True, readonly=True)
    regime_applied = fields.Selection([
        ('normal', 'Normal'),
        ('diabetic', 'Diabetic'),
        ('low_salt', 'Low Salt'),
        ('blended', 'Blended'),
        ('chopped', 'Chopped'),
        ('high_protein', 'High Protein'),
        ('renal', 'Renal'),
        ('custom', 'Custom'),
    ], string='Applied Regime')
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    state = fields.Selection([
        ('ordered', 'Ordered'),
        ('prepared', 'Prepared'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='ordered', required=True)
    billed = fields.Boolean(string='Billed', default=False)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    served_date = fields.Datetime(string='Served Date')

    def action_prepare(self):
        self.ensure_one()
        self.state = 'prepared'

    def action_serve(self):
        self.ensure_one()
        self.state = 'served'
        self.served_date = fields.Datetime.now()
        self.billed = True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'served':
            raise UserError(_('Served meals cannot be cancelled.'))
        self.state = 'cancelled'


class SfSeniorInvoiceLine(models.Model):
    _name = 'sf.senior.invoice_line'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin']
    _description = 'Resident Invoice Line'
    _order = 'period_start desc, resident_id'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    period_start = fields.Date(string='Period Start', required=True)
    period_end = fields.Date(string='Period End', required=True)
    line_type = fields.Selection([
        ('accommodation', 'Accommodation'),
        ('dependency', 'Dependency (GIR)'),
        ('care', 'Care Package'),
        ('services', 'Services/Activities'),
        ('meals', 'Meals'),
        ('other', 'Other'),
    ], string='Line Type', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Monetary(string='Unit Price', currency_field='currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id', compute='_compute_subtotal', store=True)
    gir_level_at_billing = fields.Selection([
        ('gir1', 'GIR 1'), ('gir2', 'GIR 2'), ('gir3', 'GIR 3'),
        ('gir4', 'GIR 4'), ('gir5', 'GIR 5'), ('gir6', 'GIR 6'),
    ], string='GIR Level at Billing')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit


class SfSeniorFamilyMessage(models.Model):
    _name = 'sf.senior.family_message'
    _inherit = ['sf.senior.sequence.mixin', 'sf.senior.company.mixin', 'mail.thread']
    _description = 'Family Message'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resident_id = fields.Many2one('sf.senior.resident', string='Resident', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    sender_id = fields.Many2one('res.users', string='Sender', required=True, default=lambda self: self.env.user)
    recipient_type = fields.Selection([
        ('family', 'Family'),
        ('staff', 'Staff'),
        ('all', 'All'),
    ], string='Recipient Type', required=True, default='family')
    subject = fields.Char(string='Subject', required=True)
    body = fields.Html(string='Body', required=True)
    is_read = fields.Boolean(string='Read', default=False)
    priority = fields.Selection([
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    def action_mark_read(self):
        self.ensure_one()
        self.is_read = True

    def action_mark_unread(self):
        self.ensure_one()
        self.is_read = False