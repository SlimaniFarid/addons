# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardCheckin(models.Model):
    _name = 'sf.yard.checkin'
    _description = 'Yard Gate Check-in'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'actual_arrival desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    truck_plate = fields.Char(string='Truck Plate', required=True)
    driver_name = fields.Char(string='Driver Name')
    carrier_id = fields.Many2one('res.partner', string='Carrier',
                                 ondelete='restrict')
    scheduled_arrival = fields.Datetime(string='Scheduled Arrival')
    actual_arrival = fields.Datetime(string='Actual Arrival',
                                     default=fields.Datetime.now,
                                     required=True)
    checkin_method = fields.Selection([
        ('manual', 'Manual'),
        ('qr', 'QR Code'),
    ], string='Method', default='manual')
    trailer_ids = fields.Many2many('sf.yard.trailer',
                                   'sf_yard_checkin_trailer_rel',
                                   'checkin_id', 'trailer_id',
                                   string='Trailers')
    state = fields.Selection([
        ('checked_in', 'Checked In'),
        ('at_dock', 'At Dock'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='checked_in', tracking=True, copy=False)
    checkout_id = fields.Many2one('sf.yard.checkout.wizard',
                                  string='Check-out', ondelete='set null')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.yard.checkin') or _('New')
        recs = super().create(vals_list)
        recs._register_trailers()
        return recs

    def write(self, vals):
        res = super().write(vals)
        if vals.get('trailer_ids'):
            self._register_trailers()
        return res

    def _register_trailers(self):
        """Ensure every listed trailer exists and is marked at_yard."""
        Trailer = self.env['sf.yard.trailer']
        for rec in self:
            for plate in rec.trailer_ids.mapped('name'):
                pass  # trailers already resolved as m2o records
            for trailer in rec.trailer_ids:
                if trailer.status in ('departed', False):
                    trailer.write({
                        'status': 'at_yard',
                        'arrived_at': rec.actual_arrival,
                    })

    def action_check_out(self, trailer_names=None):
        """Depart the trailers of this check-in."""
        for rec in self:
            if rec.state not in ('checked_in', 'at_dock'):
                raise UserError(_('Only active check-ins can be checked '
                                  'out.'))
            trailers = rec.trailer_ids
            if trailer_names:
                trailers = trailers.filtered(
                    lambda t: t.name in trailer_names)
            trailers.action_depart()
            rec.state = 'completed'


class SfYardCheckoutWizard(models.TransientModel):
    _name = 'sf.yard.checkout.wizard'
    _description = 'Yard Check-out'

    checkin_id = fields.Many2one('sf.yard.checkin', string='Check-in',
                                 required=True)
    trailer_ids = fields.Many2many('sf.yard.trailer', string='Trailers '
                                   'to depart')

    def action_confirm(self):
        self.ensure_one()
        self.checkin_id.action_check_out(
            trailer_names=self.trailer_ids.mapped('name'))
        return {'type': 'ir.actions.act_window_close'}
