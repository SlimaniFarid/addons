# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardTrailer(models.Model):
    _name = 'sf.yard.trailer'
    _description = 'Yard Trailer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'arrived_at desc, id desc'

    name = fields.Char(string='Trailer Ref / Plate', required=True,
                       copy=False, index=True)
    internal_ref = fields.Char(string='Internal Ref', copy=False,
                               default=lambda self: _('New'))
    trailer_type = fields.Selection([
        ('standard', 'Standard Dry Van'),
        ('reefer', 'Reefer'),
        ('curtain', 'Curtain Sider'),
        ('flatbed', 'Flatbed'),
        ('tanker', 'Tanker'),
        ('chassis', 'Container Chassis'),
    ], string='Type', default='standard', required=True)
    carrier_id = fields.Many2one('res.partner', string='Carrier',
                                 ondelete='restrict', index=True)
    owner_type = fields.Selection([
        ('own', 'Own Fleet'),
        ('carrier', 'Carrier'),
        ('customer', 'Customer'),
        ('third_party', 'Third Party'),
    ], string='Ownership', default='carrier', required=True)
    status = fields.Selection([
        ('empty', 'Empty'),
        ('loaded', 'Loaded'),
        ('at_yard', 'At Yard'),
        ('at_dock', 'At Dock'),
        ('in_shunt', 'In Shunt'),
        ('maintenance', 'Maintenance'),
        ('customs_hold', 'Customs Hold'),
        ('departed', 'Departed'),
    ], string='Status', default='at_yard', tracking=True, copy=False,
        index=True)
    current_location_id = fields.Many2one(
        'sf.yard.location', string='Current Spot', ondelete='restrict',
        tracking=True, copy=False, index=True)
    arrived_at = fields.Datetime(string='Arrived At',
                                 default=fields.Datetime.now)
    departed_at = fields.Datetime(string='Departed At', readonly=True,
                                  copy=False)
    dwell_hours = fields.Float(
        string='Dwell (h)', compute='_compute_dwell_hours')
    content_desc = fields.Char(string='Content Description')
    picking_ids = fields.Many2many('stock.picking', string='Linked Pickings')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('sf_yard_trailer_name_uniq',
         'unique(name, company_id)',
         'Trailer reference must be unique per company.'),
    ]

    @api.depends('arrived_at', 'departed_at', 'status')
    def _compute_dwell_hours(self):
        now = fields.Datetime.now()
        for t in self:
            if not t.arrived_at:
                t.dwell_hours = 0.0
                continue
            end = t.departed_at or (
                now if t.status != 'departed' else t.departed_at)
            delta = (end - t.arrived_at).total_seconds() / 3600.0
            t.dwell_hours = max(0.0, delta)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('internal_ref') or \
                    vals['internal_ref'] == _('New'):
                vals['internal_ref'] = self.env['ir.sequence'].next_by_code(
                    'sf.yard.trailer') or _('New')
            if vals.get('status', 'at_yard') != 'at_yard':
                raise UserError(_(
                    'Trailers enter the yard with status At Yard.'))
        return super().create(vals_list)

    def write(self, vals):
        if 'current_location_id' in vals:
            new_loc_id = vals['current_location_id']
            for rec in self:
                if new_loc_id:
                    loc = self.env['sf.yard.location'].browse(new_loc_id)
                    if loc.trailer_id and loc.trailer_id.id != rec.id:
                        raise UserError(_(
                            'Spot %s is already occupied by %s.')
                            % (loc.name, loc.trailer_id.name))
                    if rec.current_location_id and \
                            rec.current_location_id.id != new_loc_id:
                        rec.current_location_id.trailer_id = False
        return super().write(vals)

    def unlink(self):
        moved = self.filtered(
            lambda t: t.shunt_ids or t.detention_ids)
        if moved:
            raise UserError(_(
                'Trailers with shunt or detention history cannot be '
                'deleted. Archive them instead.'))
        return super().unlink()

    def action_assign_dock(self, dock_location):
        self.ensure_one()
        if dock_location.occupied and \
                dock_location.trailer_id.id != self.id:
            raise UserError(_('Dock %s is occupied.')
                            % dock_location.name)
        self.write({
            'current_location_id': dock_location.id,
            'status': 'at_dock',
        })

    def action_depart(self):
        for trailer in self:
            open_det = trailer.detention_ids.filtered(
                lambda d: d.status in ('warning', 'chargeable'))
            if open_det:
                trailer._notify_open_detention(open_det)
            if trailer.current_location_id:
                trailer.current_location_id.trailer_id = False
            trailer.write({
                'status': 'departed',
                'departed_at': fields.Datetime.now(),
                'current_location_id': False,
            })

    def _notify_open_detention(self, detentions):
        todo = self.env.ref('mail.mail_activity_data_todo',
                            raise_if_not_found=False)
        existing = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', todo.id if todo else False),
            ('done', '=', False),
            ('summary', '=', 'Departed with unpaid detention'),
        ], limit=1)
        if existing:
            return
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            summary='Departed with unpaid detention',
            note=_('%d detention line(s) still chargeable on %s.')
            % (len(detentions), self.name),
        )
