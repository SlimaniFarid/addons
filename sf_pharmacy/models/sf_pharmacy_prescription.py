# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class PharmacyPrescription(models.Model):
    _name = 'sf.pharmacy.prescription'
    _description = 'Prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'prescription_date desc, id desc'

    name = fields.Char(string='Prescription', readonly=True)
    patient_name = fields.Char(string='Patient')
    prescriber = fields.Char(string='Prescriber')
    prescription_date = fields.Date(string='Prescription date', default=fields.Date.context_today)
    dispensation_ids = fields.One2many('sf.pharmacy.dispensation', 'prescription_id', string='Dispensations')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, ondelete='cascade')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.prescription')
        return super(PharmacyPrescription, self).create(vals)

    def unlink(self):
        if any(rec.state != 'draft' for rec in self):
            self._check_manager()
        return super(PharmacyPrescription, self).unlink()

    def _check_manager(self):
        if not self.env.user.has_group('sf_pharmacy.group_sf_pharmacy_manager'):
            raise AccessError(_('Action reserved for the manager group.'))

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only a draft prescription can be confirmed.'))
            for line in rec.dispensation_ids:
                if line.state != 'draft':
                    continue
                if not line.qty or line.qty <= 0:
                    raise UserError(_('Any unsold dispensation blocks the confirmation.'))
                if not line.batch_id:
                    raise UserError(_('A batch must be selected for each dispensation.'))
                if line.batch_id.status in ('expired', 'withdrawn', 'recalled'):
                    raise UserError(_('Dispensation forbidden on an expired, withdrawn or recalled batch.'))
                if line.qty > line.batch_id.qty_available:
                    raise UserError(_('Insufficient stock quantity for the batch.'))
            rec.state = 'confirmed'
        return True

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('The prescription must be confirmed before being marked as done.'))
            for line in rec.dispensation_ids:
                if line.state in ('done', 'cancelled'):
                    continue
                line.action_done()
            rec.state = 'done'
        return True

    def action_cancel(self):
        for rec in self:
            rec.dispensation_ids.filtered(lambda l: l.state == 'draft').write({'state': 'cancelled'})
            rec.state = 'cancelled'
        return True
