# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityMeter(models.Model):
    _name = 'sf.utility.meter'
    _description = 'Utility Meter'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.utility.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    address_id = fields.Many2one('res.partner', string='Delivery Address', ondelete='set null')
    utility_type = fields.Selection([
        ('water', 'Water'),
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('heating', 'Heating'),
        ('other', 'Other'),
    ], string='Utility Type', required=True, default='water')
    serial = fields.Char(string='Serial Number')
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure')
    opening_index = fields.Float(string='Opening Index')
    active = fields.Boolean(string='Active', default=True)
    reading_ids = fields.One2many('sf.utility.meter.reading', 'meter_id', string='Readings')
    invoice_ids = fields.One2many('sf.utility.invoice', 'meter_id', string='Invoices')
    last_index = fields.Float(string='Last Index', compute='_compute_last_index', store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('reading_ids.state', 'reading_ids.index', 'reading_ids.reading_date')
    def _compute_last_index(self):
        for meter in self:
            validated = meter.reading_ids.filtered(lambda r: r.state == 'validated')
            if validated:
                latest = validated.sorted(key=lambda r: (r.reading_date, r.id))[-1]
                meter.last_index = latest.index
            else:
                meter.last_index = meter.opening_index or 0.0

    def _check_manager(self):
        if not self.env.user.has_group('sf_utility_billing.group_sf_utility_manager'):
            raise UserError(_('Only a utility manager can perform this action.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.utility.meter')
            if not vals.get('unit_of_measure'):
                unit = self.env.ref('uom.product_uom_unit', raise_if_not_found=False)
                if unit:
                    vals['unit_of_measure'] = unit.id
        return super().create(vals_list)

    def _sf_check_anomaly(self, reading):
        self.ensure_one()
        threshold = float(self.env['ir.config_parameter'].sudo().get_param(
            'sf_utility_billing.anomaly_threshold', '500.0'))
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        if reading.consumption > threshold:
            return self._sf_check_todo(
                todo_type,
                'Abnormal consumption on %s' % self.name,
                'Reading %s shows a consumption of %s units, above the configured threshold.' % (
                    reading.name, reading.consumption),
            )
        return None