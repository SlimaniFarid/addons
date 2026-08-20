# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class RouteTour(models.Model):
    _name = 'sf.route.tour'
    _description = 'Sales Route'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'date desc'

    name = fields.Char(string='Name', required=True,
                       default=lambda self: _('New'))
    date = fields.Date(string='Date', required=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson',
                                     required=True,
                                     default=lambda self: self.env.user)
    territory_id = fields.Many2one('sf.route.territory',
                                   string='Territory')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    visit_ids = fields.One2many('sf.route.visit', 'tour_id',
                                string='Visits')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.onchange('territory_id')
    def _onchange_territory(self):
        if self.territory_id and self.territory_id.salesperson_id:
            self.salesperson_id = self.territory_id.salesperson_id

    def action_plan(self):
        for tour in self:
            if tour.state != 'draft':
                raise UserError(_('Only draft tours can be planned.'))
            tour.state = 'planned'
            tour.message_post(body=_('Tour planned.'))

    def action_start(self):
        for tour in self:
            if tour.state != 'planned':
                raise UserError(
                    _('Only planned tours can be started.'))
            tour.state = 'in_progress'
            tour.message_post(body=_('Tour started.'))

    def action_complete(self):
        for tour in self:
            if tour.state != 'in_progress':
                raise UserError(
                    _('Only in-progress tours can be completed.'))
            tour.state = 'completed'
            tour.message_post(body=_('Tour completed.'))

    def action_cancel(self):
        for tour in self:
            if tour.state not in ('draft', 'planned'):
                raise UserError(
                    _('Only draft or planned tours can be cancelled.'))
            tour.state = 'cancelled'
            tour.message_post(body=_('Tour cancelled.'))

    def unlink(self):
        for tour in self:
            if tour.state in ('in_progress', 'completed'):
                raise UserError(
                    _('An active or completed tour cannot be deleted.'))
        return super().unlink()


class RouteVisit(models.Model):
    _name = 'sf.route.visit'
    _description = 'Route Visit'
    _order = 'sequence, planned_time'

    tour_id = fields.Many2one('sf.route.tour', string='Tour',
                              ondelete='cascade', required=True)
    sequence = fields.Integer(string='Sequence')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True)
    planned_time = fields.Datetime(string='Planned Time')
    check_in = fields.Datetime(string='Check-In')
    check_out = fields.Datetime(string='Check-Out')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', tracking=True)
    result = fields.Selection([
        ('order', 'Order'),
        ('opportunity', 'Opportunity'),
        ('information', 'Information'),
        ('not_interested', 'Not Interested'),
    ], string='Result')
    comment = fields.Text(string='Comment')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity')
    company_id = fields.Many2one(related='tour_id.company_id',
                                 string='Company', store=True)

    _sql_constraints = [
        ('tour_partner_uniq', 'UNIQUE (tour_id, partner_id)',
         'A customer can only be visited once per tour.'),
    ]

    def action_check_in(self):
        for visit in self:
            if visit.state != 'planned':
                raise UserError(_('Only planned visits can be checked '
                                  'in.'))
            visit.check_in = fields.Datetime.now()
            visit.state = 'in_progress'
            visit.tour_id.message_post(body=_(
                'Check-in for %s.') % visit.partner_id.name)

    def action_check_out(self):
        for visit in self:
            if visit.state != 'in_progress':
                raise UserError(
                    _('Only in-progress visits can be checked out.'))
            if visit.check_in and visit.check_out and \
                    visit.check_out < visit.check_in:
                raise UserError(
                    _('Check-out cannot be before check-in.'))
            visit.check_out = fields.Datetime.now()
            visit.state = 'done'
            visit.tour_id.message_post(body=_(
                'Check-out for %s.') % visit.partner_id.name)

    def action_mark_missed(self):
        for visit in self:
            if visit.state != 'planned':
                raise UserError(
                    _('Only planned visits can be marked as missed.'))
            visit.state = 'missed'

    def action_cancel_visit(self):
        for visit in self:
            if visit.state != 'planned':
                raise UserError(
                    _('Only planned visits can be cancelled.'))
            visit.state = 'cancelled'

    def action_create_order(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(
                _('Only completed visits can create an order.'))
        order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
        })
        self.sale_order_id = order.id
        self.result = 'order'
        self.tour_id.message_post(body=_(
            'Sale order %s created from visit.') % order.name)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id,
            'view_mode': 'form',
        }

    def action_create_opportunity(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(
                _('Only completed visits can create an opportunity.'))
        lead = self.env['crm.lead'].create({
            'name': self.partner_id.name,
            'partner_id': self.partner_id.id,
        })
        self.opportunity_id = lead.id
        self.result = 'opportunity'
        self.tour_id.message_post(body=_(
            'Opportunity created from visit.'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'res_id': lead.id,
            'view_mode': 'form',
        }

    @api.model
    def _check_missed_visits(self):
        today = fields.Date.today()
        tours = self.env['sf.route.tour'].search([
            ('date', '<', today),
            ('state', 'in', ('planned', 'in_progress')),
        ])
        for tour in tours:
            missed = tour.visit_ids.filtered(lambda v: v.state == 'planned')
            if missed:
                missed.action_mark_missed()