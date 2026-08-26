# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WorkshopVehicle(models.Model):
    _name = 'sf.workshop.vehicle'
    _description = 'Workshop Vehicle'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    license_plate = fields.Char(string='License plate', index=True)
    brand = fields.Char(string='Brand')
    model = fields.Char(string='Model')
    owner = fields.Char(string='Owner')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='restrict')
    odometer = fields.Float(string='Odometer (km)', default=0.0)
    order_ids = fields.One2many('sf.workshop.order', 'vehicle_id',
                                string='Repair orders')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.workshop.vehicle')
        return super().create(vals)


class WorkshopRequest(models.Model):
    _name = 'sf.workshop.request'
    _description = 'Workshop Request'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    vehicle_id = fields.Many2one('sf.workshop.vehicle', string='Vehicle',
                                 required=True, ondelete='restrict',
                                 index=True)
    requester = fields.Char(string='Requester')
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.workshop.request')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_vehicle_workshop.group_sf_workshop_manager'):
            raise UserError(_('Only a workshop manager can assign a '
                              'request.'))

    def action_assign(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'draft':
            raise UserError(_('Only draft requests can be assigned.'))
        self.state = 'assigned'

    def action_start(self):
        self.ensure_one()
        if self.state != 'assigned':
            raise UserError(_('Only assigned requests can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress requests can be marked as '
                              'done.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ('draft', 'assigned'):
            raise UserError(_('Only draft or assigned requests can be '
                              'cancelled.'))
        self.state = 'cancelled'

    @api.model
    def _check_workshop_alerts(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            cutoff = fields.Datetime.to_datetime(today) - timedelta(
                days=company.sf_workshop_alert_days)
            requests = self.with_company(company).search([
                ('priority', 'in', ['high', 'urgent']),
                ('state', '=', 'draft'),
                ('create_date', '<', cutoff),
                ('company_id', '=', company.id),
            ])
            for request in requests:
                existing = request.activity_ids.filtered(
                    lambda a: a.activity_type_id == self.env.ref(
                        'mail.mail_activity_data_todo') and a.state != 'done')
                if existing:
                    continue
                request.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Urgent request %s is not assigned yet')
                    % request.name,
                    user_id=self.env.user.id)
            orders = self.env['sf.workshop.order'].with_company(
                company).search([
                    ('planned_end', '!=', False),
                    ('planned_end', '<', today),
                    ('state', 'not in', ['done', 'closed']),
                    ('company_id', '=', company.id),
                ])
            for order in orders:
                existing = order.activity_ids.filtered(
                    lambda a: a.activity_type_id == self.env.ref(
                        'mail.mail_activity_data_todo') and a.state != 'done')
                if existing:
                    continue
                order.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Repair order %s is overdue') % order.name,
                    user_id=self.env.user.id)


class WorkshopOrder(models.Model):
    _name = 'sf.workshop.order'
    _description = 'Workshop Repair Order'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    request_id = fields.Many2one('sf.workshop.request', string='Request',
                                 ondelete='restrict')
    vehicle_id = fields.Many2one('sf.workshop.vehicle', string='Vehicle',
                                 required=True, ondelete='restrict',
                                 index=True)
    mechanic_ids = fields.Many2many('res.users', string='Mechanics')
    planned_start = fields.Datetime(string='Planned start')
    planned_end = fields.Date(string='Planned end')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    operation_ids = fields.One2many('sf.workshop.operation', 'order_id',
                                    string='Operations')
    part_ids = fields.One2many('sf.workshop.part', 'order_id',
                               string='Parts')
    parts_total = fields.Float(string='Parts total',
                               compute='_compute_total_cost', store=True)
    labor_total = fields.Float(string='Labor total',
                               compute='_compute_total_cost', store=True)
    total_cost = fields.Float(string='Total cost',
                              compute='_compute_total_cost', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('part_ids.total', 'operation_ids.hours',
                 'company_id.sf_workshop_hourly_rate')
    def _compute_total_cost(self):
        for order in self:
            parts = sum(order.part_ids.mapped('total'))
            labor = sum(
                (op.hours or 0.0)
                * order.company_id.sf_workshop_hourly_rate
                for op in order.operation_ids)
            order.parts_total = parts
            order.labor_total = labor
            order.total_cost = parts + labor

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.workshop.order')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_vehicle_workshop.group_sf_workshop_manager'):
            raise UserError(_('Only a workshop manager can close a repair '
                              'order.'))

    def action_plan(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft orders can be planned.'))
        self.state = 'planned'

    def action_start(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned orders can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress orders can be marked as '
                              'done.'))
        self.state = 'done'

    def action_close(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'done':
            raise UserError(_('Only done orders can be closed.'))
        self.state = 'closed'


class WorkshopOperation(models.Model):
    _name = 'sf.workshop.operation'
    _description = 'Workshop Operation'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    order_id = fields.Many2one('sf.workshop.order', string='Repair order',
                               required=True, ondelete='cascade',
                               index=True)
    operation_type = fields.Selection([
        ('diagnostic', 'Diagnostic'),
        ('mechanical', 'Mechanical'),
        ('bodywork', 'Bodywork'),
        ('electrical', 'Electrical'),
        ('other', 'Other'),
    ], string='Operation type', default='mechanical', required=True)
    description = fields.Text(string='Description')
    hours = fields.Float(string='Hours', default=0.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.workshop.operation')
        return super().create(vals)

    def action_plan(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft operations can be planned.'))
        self.state = 'planned'

    def action_done(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned operations can be marked as '
                              'done.'))
        self.state = 'done'


class WorkshopPart(models.Model):
    _name = 'sf.workshop.part'
    _description = 'Workshop Part'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    order_id = fields.Many2one('sf.workshop.order', string='Repair order',
                               required=True, ondelete='cascade',
                               index=True)
    part_name = fields.Char(string='Part name', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Float(string='Unit price', default=0.0,
                              required=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('installed', 'Installed'),
    ], string='Status', default='draft', required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for part in self:
            part.total = part.quantity * part.unit_price

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.workshop.part')
        return super().create(vals)

    def action_order(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft parts can be ordered.'))
        self.state = 'ordered'

    def action_install(self):
        self.ensure_one()
        if self.state != 'ordered':
            raise UserError(_('Only ordered parts can be installed.'))
        self.state = 'installed'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.workshop.vehicle'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

