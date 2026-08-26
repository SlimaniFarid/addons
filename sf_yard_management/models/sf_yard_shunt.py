# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardShuntMove(models.Model):
    _name = 'sf.yard.shunt.move'
    _description = 'Yard Shunt Move (Jockey)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'requested_at desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    trailer_id = fields.Many2one('sf.yard.trailer', string='Trailer',
                                 required=True, ondelete='restrict',
                                 index=True)
    from_location_id = fields.Many2one('sf.yard.location',
                                       string='From Spot')
    to_location_id = fields.Many2one('sf.yard.location', string='To Spot',
                                     required=True)
    tractor_ref = fields.Char(string='Tractor / Jockey Ref')
    driver_name = fields.Char(string='Jockey Driver')
    priority = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('cold_chain', 'Cold Chain'),
    ], string='Priority', default='normal', required=True)
    state = fields.Selection([
        ('requested', 'Requested'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='requested', tracking=True, copy=False,
        index=True)
    requested_at = fields.Datetime(string='Requested At',
                                   default=fields.Datetime.now,
                                   required=True)
    started_at = fields.Datetime(string='Started At', readonly=True,
                                 copy=False)
    completed_at = fields.Datetime(string='Completed At', readonly=True,
                                   copy=False)
    duration_minutes = fields.Integer(
        string='Duration (min)', compute='_compute_duration', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    @api.depends('started_at', 'completed_at')
    def _compute_duration(self):
        for m in self:
            if m.started_at and m.completed_at:
                delta = (m.completed_at - m.started_at).total_seconds() / 60.0
                m.duration_minutes = int(round(delta))
            else:
                m.duration_minutes = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.yard.shunt.move') or _('New')
            if vals.get('from_location_id') and \
                    vals.get('to_location_id') and \
                    vals['from_location_id'] == vals['to_location_id']:
                raise UserError(_('Origin and destination must differ.'))
            trailer = self.env['sf.yard.trailer'].browse(
                vals.get('trailer_id'))
            if trailer and trailer.status == 'in_shunt':
                raise UserError(_(
                    'Trailer %s is already in a shunt move.')
                    % trailer.name)
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals:
            flow = {
                'requested': {'requested', 'assigned', 'cancelled'},
                'assigned': {'assigned', 'in_progress', 'cancelled'},
                'in_progress': {'in_progress', 'completed'},
                'completed': {'completed'},
                'cancelled': {'cancelled'},
            }
            for rec in self:
                if vals['state'] not in flow.get(rec.state, set()):
                    raise UserError(_(
                        'Invalid shunt transition %s -> %s.')
                        % (rec.state, vals['state']))
        return super().write(vals)

    def unlink(self):
        if any(rec.state not in ('requested', 'cancelled') for rec in self):
            raise UserError(_('Only requested or cancelled shunts can be '
                              'deleted.'))
        return super().unlink()

    def action_assign(self, tractor_ref=None, driver_name=None):
        for m in self:
            if m.state != 'requested':
                raise UserError(_('Only requested moves can be assigned.'))
            vals = {'state': 'assigned'}
            if tractor_ref:
                vals['tractor_ref'] = tractor_ref
            if driver_name:
                vals['driver_name'] = driver_name
            m.write(vals)

    def action_start(self):
        for m in self:
            if m.state != 'assigned':
                raise UserError(_('Only assigned moves can start.'))
            dest = m.to_location_id
            if dest.occupied and dest.trailer_id.id != m.trailer_id.id:
                raise UserError(_('Destination spot %s is occupied.')
                                % dest.name)
            m.write({
                'state': 'in_progress',
                'started_at': fields.Datetime.now(),
            })
            m.trailer_id.write({'status': 'in_shunt'})

    def action_complete(self):
        for m in self:
            if m.state != 'in_progress':
                raise UserError(_('Only in-progress moves can complete.'))
            old_loc = m.trailer_id.current_location_id
            if old_loc and old_loc.id != m.to_location_id.id:
                old_loc.trailer_id = False
            m.to_location_id.trailer_id = m.trailer_id.id
            new_status = ('at_dock'
                          if m.to_location_id.location_type == 'dock'
                          else 'at_yard')
            m.trailer_id.write({
                'current_location_id': m.to_location_id.id,
                'status': new_status,
            })
            m.write({
                'state': 'completed',
                'completed_at': fields.Datetime.now(),
            })
