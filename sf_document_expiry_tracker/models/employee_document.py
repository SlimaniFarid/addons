# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EmployeeDocument(models.Model):
    _name = 'sf.document.expiry.tracker.employee.document'
    _description = 'Employee Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    employee_id = fields.Many2one(required=True, comodel_name='hr.employee', ondelete='restrict')
    doc_type = fields.Selection([
        ('passport', 'Passport'),
        ('id_card', 'ID Card'),
        ('work_permit', 'Work Permit'),
        ('visa', 'Visa'),
        ('medical_check', 'Medical Check'),
        ('certification', 'Certification'),
        ('driving_licence', 'Driving Licence'),
        ('other', 'Other'),
        ], string='Document Type', required=True)
    expiry_date = fields.Date(string='Expiry Date', required=True)
    reminder_days = fields.Integer(string='Reminder Days', default=30)
    attachment_id = fields.Many2one(comodel_name='ir.attachment', ondelete='restrict')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Valid'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='valid', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.document.expiry.tracker.employee.document') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()
    
    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.document.expiry.tracker.employee.document'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

