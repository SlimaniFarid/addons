# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class PharmacyPrescription(models.Model):
    _name = 'sf.pharmacy.prescription'
    _description = 'Ordonnance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'prescription_date desc, id desc'

    name = fields.Char(string='Ordonnance', readonly=True)
    patient_name = fields.Char(string='Patient')
    prescriber = fields.Char(string='Prescripteur')
    prescription_date = fields.Date(string='Date de prescription', default=fields.Date.context_today)
    dispensation_ids = fields.One2many('sf.pharmacy.dispensation', 'prescription_id', string='Délivrances')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], string='Statut', default='draft')
    company_id = fields.Many2one('res.company', string='Société', default=lambda self: self.env.company, ondelete='cascade')

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
            raise AccessError(_('Action réservée au groupe manager.'))

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Seule une ordonnance brouillon peut être confirmée.'))
            for line in rec.dispensation_ids:
                if line.state != 'draft':
                    continue
                if not line.qty or line.qty <= 0:
                    raise UserError(_('Toute délivrance non soldée est bloquée à la confirmation.'))
                if not line.batch_id:
                    raise UserError(_('Un lot doit être sélectionné pour chaque délivrance.'))
                if line.batch_id.status in ('expired', 'withdrawn', 'recalled'):
                    raise UserError(_('Délivrance interdite sur un lot périmé, retiré ou rappelé.'))
                if line.qty > line.batch_id.qty_available:
                    raise UserError(_('Quantité insuffisante en stock pour le lot.'))
            rec.state = 'confirmed'
        return True

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('L\'ordonnance doit être confirmée avant d\'être terminée.'))
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
