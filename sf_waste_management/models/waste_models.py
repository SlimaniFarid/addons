# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class WasteSite(models.Model):
    _name = 'sf.waste.site'
    _description = 'Waste Production Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    site_code = fields.Char(string='Site code')
    address = fields.Char(string='Address')
    manager_id = fields.Many2one('res.users', string='Site manager')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This site already exists.')),
    ]


class WasteCode(models.Model):
    _name = 'sf.waste.code'
    _description = 'Waste Code'
    _order = 'name'

    name = fields.Char(string='Code', required=True)
    description = fields.Char(string='Description')
    hazardous = fields.Boolean(string='Hazardous')
    category = fields.Char(string='Category')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This waste code already exists.')),
    ]


class WasteBsd(models.Model):
    _name = 'sf.waste.bsd'
    _description = 'Waste Tracking Slip (BSD)'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    site_id = fields.Many2one('sf.waste.site', string='Site', required=True,
                              ondelete='restrict', index=True)
    waste_code_id = fields.Many2one('sf.waste.code', string='Waste code',
                                    required=True, ondelete='restrict',
                                    index=True)
    quantity_kg = fields.Float(string='Quantity (kg)', required=True)
    collector_id = fields.Many2one('res.partner', string='Collector',
                                   ondelete='restrict')
    destination_id = fields.Many2one('res.partner', string='Destination',
                                     ondelete='restrict')
    emit_date = fields.Date(string='Emission date')
    expected_reception_date = fields.Date(string='Expected reception',
                                          index=True)
    reception_date = fields.Date(string='Reception date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('emitted', 'Emitted'),
        ('transferred', 'Transferred'),
        ('received', 'Received'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This BSD number already exists.')),
        ('quantity_positive', 'CHECK(quantity_kg > 0)',
         _('The quantity must be positive.')),
    ]

    @api.constrains('emit_date', 'reception_date')
    def _check_dates(self):
        for bsd in self:
            if bsd.emit_date and bsd.reception_date and \
                    bsd.reception_date < bsd.emit_date:
                raise ValidationError(_('The reception date cannot be '
                                        'before the emission date.'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.waste.bsd')
            vals['name'] = 'BSD-%s' % seq
        return super().create(vals)

    def action_emit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft slips can be emitted.'))
        self.write({
            'emit_date': self.emit_date or fields.Date.today(),
            'state': 'emitted',
        })

    def action_transfer(self):
        self.ensure_one()
        if self.state != 'emitted':
            raise UserError(_('Only emitted slips can be transferred.'))
        self.state = 'transferred'

    def action_receive(self):
        self.ensure_one()
        if self.state != 'transferred':
            raise UserError(_('Only transferred slips can be confirmed as '
                              'received.'))
        self.write({
            'reception_date': self.reception_date or fields.Date.today(),
            'state': 'received',
        })

    def action_archive(self):
        self.ensure_one()
        if self.state != 'received':
            raise UserError(_('Only received slips can be archived.'))
        self.state = 'archived'

    def action_cancel(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft slips can be cancelled.'))
        self.state = 'cancelled'

    def unlink(self):
        for bsd in self:
            if bsd.state != 'draft':
                raise UserError(_('An emitted or later slip cannot be '
                                  'deleted.'))
        return super().unlink()

    def _check_reception_overdue(self):
        today = fields.Date.today()
        slips = self.search([('state', 'in', ('emitted', 'transferred')),
                             ('expected_reception_date', '!=', False)])
        for bsd in slips:
            limit = bsd.expected_reception_date + \
                bsd.company_id.sf_waste_alert_days
            if today > limit and bsd.site_id.manager_id:
                bsd.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('BSD %s reception overdue') % (bsd.name,),
                    user_id=bsd.site_id.manager_id.id)