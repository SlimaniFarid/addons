# -*- coding: utf-8 -*-
"""Quality Alert Aging Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQalertAging(models.Model):
    _name = 'sf.qalert.aging'
    _description = 'Alert Aging Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    alert_ref = fields.Char(string='Alert Ref', required=True)
    opened_date = fields.Date(string='Opened', required=True)
    owner_id = fields.Many2one('res.users', string='Owner')
    aging_days = fields.Integer(string='Aging (days)')
    escalation_level = fields.Selection([
        ('none', 'None'),
        ('manager', 'Manager'),
        ('director', 'Director'),
        ], string='Escalation', default='none')
    blocker = fields.Text(string='Blocker')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('escalated', 'Escalated'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.qalert.aging') or 'NEW'
        return super().create(vals_list)

    def action_escalated(self):
        self.write({'state': 'escalated'})

    def action_closed(self):
        self.write({'state': 'closed'})


# --- wave2 ---
class _Wave2QAging(models.Model):
    _inherit = 'sf.qalert.aging'

    def action_sync_alerts(self):
        """Import open native quality alerts with live ageing + escalation."""
        Alert = self.env['quality.alert']
        self.ensure_one()
        today = fields.Date.context_today(self)
        alerts = Alert.search([('stage_id.fold', '=', False)])
        existing = {r.alert_ref: r for r in self.search([])}
        created = updated = 0
        for al in alerts:
            opened = fields.Date.to_date(al.create_date)
            age = (today - opened).days
            esc = ('director' if age > 30 else
                   'manager' if age > 14 else
                   'none' if age <= 7 else 'manager')
            vals = {'opened_date': opened, 'aging_days': age,
                    'escalation_level': esc}
            key = al.name
            rec = existing.get(key)
            if rec:
                rec.write(vals)
                updated += 1
            else:
                vals.update({'alert_ref': key, 'name': al.name})
                self.create(vals)
                created += 1
        self.message_post(body=_('Alert sync: %s created, %s updated.')
                          % (created, updated))
        return True

