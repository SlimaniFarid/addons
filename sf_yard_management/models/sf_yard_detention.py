# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardDetention(models.Model):
    _name = 'sf.yard.detention'
    _description = 'Yard Detention / Demurrage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'arrived_at desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       default=lambda self: _('New'))
    trailer_id = fields.Many2one('sf.yard.trailer', string='Trailer',
                                 required=True, ondelete='cascade',
                                 index=True)
    carrier_id = fields.Many2one(related='trailer_id.carrier_id',
                                 store=True)
    free_time_hours = fields.Float(string='Free Time (h)', default=2.0)
    rate_per_hour = fields.Monetary(string='Rate per Hour',
                                    currency_field='currency_id')
    arrived_at = fields.Datetime(related='trailer_id.arrived_at', store=True)
    hours_detained = fields.Float(string='Hours in Yard', default=0.0)
    billable_hours = fields.Float(
        string='Billable Hours', compute='_compute_billable', store=True)
    total_amount = fields.Monetary(
        string='Detention Amount', currency_field='currency_id',
        compute='_compute_billable', store=True)
    currency_id = fields.Many2one(
        related='company_id.currency_id')
    status = fields.Selection([
        ('within_free', 'Within Free Time'),
        ('warning', 'Warning (80%)'),
        ('chargeable', 'Chargeable'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    ], string='Status', default='within_free', tracking=True,
        copy=False, index=True)
    invoice_id = fields.Many2one('account.move', string='Invoice',
                                 ondelete='set null', readonly=True,
                                 copy=False)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)

    @api.depends('hours_detained', 'free_time_hours', 'rate_per_hour')
    def _compute_billable(self):
        for d in self:
            billable = max(0.0, d.hours_detained - d.free_time_hours)
            d.billable_hours = billable
            d.total_amount = billable * (d.rate_per_hour or 0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.yard.detention') or _('New')
            trailer = self.env['sf.yard.trailer'].browse(
                vals.get('trailer_id'))
            if trailer and trailer.carrier_id:
                partner = trailer.carrier_id
                if not vals.get('free_time_hours'):
                    vals['free_time_hours'] = partner.sf_yard_free_hours
                if not vals.get('rate_per_hour'):
                    vals['rate_per_hour'] = \
                        partner.sf_yard_rate_per_hour
        return super().create(vals_list)

    def unlink(self):
        if any(rec.status == 'invoiced' for rec in self):
            raise UserError(_('Invoiced detentions cannot be deleted.'))
        return super().unlink()

    def action_waive(self):
        self.write({'status': 'waived'})

    @api.model
    def _cron_update_detention(self):
        """Hourly: refresh hours, transition statuses, notify. Idempotent."""
        now = fields.Datetime.now()
        companies = self.env['res.company'].search([])
        for company in companies:
            Detention = self.with_company(company)
            active = Detention.search([
                ('status', 'in', ('within_free', 'warning', 'chargeable')),
                ('company_id', '=', company.id),
            ])
            trailers_active = active.mapped('trailer_id').filtered(
                lambda t: t.status != 'departed')
            active = active.filtered(lambda d: d.trailer_id in
                                     trailers_active)
            for d in active:
                if not d.arrived_at:
                    continue
                hours = (now - d.arrived_at).total_seconds() / 3600.0
                d.hours_detained = max(0.0, hours)
                threshold_warn = d.free_time_hours * 0.8
                new_status = d.status
                if d.hours_detained >= d.free_time_hours > 0:
                    new_status = 'chargeable'
                elif d.free_time_hours > 0 and \
                        d.hours_detained >= threshold_warn:
                    new_status = 'warning'
                if new_status != d.status:
                    d.status = new_status
                if new_status in ('warning', 'chargeable'):
                    d._ensure_activity(new_status)

    def _ensure_activity(self, kind):
        todo = self.env.ref('mail.mail_activity_data_todo',
                            raise_if_not_found=False)
        summary = _('Detention warning (80%% of free time)') \
            if kind == 'warning' else _('Detention chargeable')
        existing = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', todo.id if todo else False),
            ('done', '=', False),
            ('summary', '=', summary),
        ], limit=1)
        if existing:
            return
        manager_group = self.env.ref(
            'sf_yard_management.group_sf_yard_manager',
            raise_if_not_found=False)
        users = manager_group.users if manager_group else self.env.user
        self.activity_schedule(
            'mail.mail_activity_data_todo',
            user_id=(users[:1] or self.env.user).id,
            summary=summary,
            note=_('Trailer %s — %.1fh in yard (%.1fh billable).')
            % (self.trailer_id.name, self.hours_detained,
               self.billable_hours),
        )
