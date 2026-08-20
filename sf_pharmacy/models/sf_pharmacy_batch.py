# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class PharmacyBatch(models.Model):
    _name = 'sf.pharmacy.batch'
    _description = 'Pharmaceutical batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'expiry_date, id'

    name = fields.Char(string='Batch', readonly=True)
    product_id = fields.Many2one('sf.pharmacy.product', string='Product', required=True, ondelete='cascade', index=True)
    lot_ref = fields.Char(string='Supplier reference')
    expiry_date = fields.Date(string='Expiry date', required=True)
    qty_received = fields.Float(string='Received quantity', default=0.0)
    qty_dispensed = fields.Float(string='Dispensed quantity', compute='_compute_quantities', store=True)
    qty_reserved = fields.Float(string='Reserved quantity', default=0.0)
    qty_withdrawn = fields.Float(string='Withdrawn quantity', compute='_compute_quantities', store=True)
    qty_available = fields.Float(string='Available quantity', compute='_compute_quantities', store=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('expired', 'Expired'),
        ('recalled', 'Recalled'),
        ('withdrawn', 'Withdrawn'),
    ], string='Status', compute='_compute_quantities', store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, ondelete='cascade')
    movement_ids = fields.One2many('sf.pharmacy.batch_movement', 'batch_id', string='Movements')

    @api.depends('qty_received', 'qty_reserved', 'expiry_date',
                 'movement_ids.movement_type', 'movement_ids.qty')
    def _compute_quantities(self):
        totals = {}
        for rec in self:
            totals.setdefault(rec.id, {'out': 0.0, 'withdrawn': 0.0, 'has_withdrawal': False, 'has_recall': False})
        moves = self.env['sf.pharmacy.batch_movement'].search([('batch_id', 'in', self.ids)])
        for move in moves:
            row = totals[move.batch_id.id]
            if move.movement_type == 'out':
                row['out'] += move.qty
            elif move.movement_type == 'withdrawal':
                row['withdrawn'] += move.qty
                row['has_withdrawal'] = True
            elif move.movement_type == 'recall':
                row['withdrawn'] += move.qty
                row['has_recall'] = True
        today = fields.Date.today()
        for rec in self:
            row = totals[rec.id]
            qty_dispensed = row['out']
            qty_withdrawn = row['withdrawn']
            qty_available = rec.qty_received - qty_dispensed - rec.qty_reserved - qty_withdrawn
            if row['has_withdrawal']:
                status = 'withdrawn'
            elif row['has_recall']:
                status = 'recalled'
            elif rec.expiry_date and rec.expiry_date < today:
                status = 'expired'
            else:
                status = 'available'
            rec.update({
                'qty_dispensed': qty_dispensed,
                'qty_withdrawn': qty_withdrawn,
                'qty_available': qty_available,
                'status': status,
            })

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.pharmacy.batch')
        return super(PharmacyBatch, self).create(vals)

    def write(self, vals):
        res = super(PharmacyBatch, self).write(vals)
        for rec in self:
            if rec.qty_available < 0:
                raise UserError(_('Negative stock is not allowed.'))
        return res

    def unlink(self):
        if any(rec.movement_ids for rec in self):
            self._check_manager()
        return super(PharmacyBatch, self).unlink()

    def _check_manager(self):
        if not self.env.user.has_group('sf_pharmacy.group_sf_pharmacy_manager'):
            raise AccessError(_('Action reserved for the manager group.'))

    @api.model
    def _get_fifo_batch(self, product_id, qty=0.0, company_id=None):
        domain = [
            ('product_id', '=', product_id),
            ('status', '=', 'available'),
            ('qty_available', '>', 0.0),
        ]
        if company_id:
            domain.append(('company_id', '=', company_id))
        return self.search(domain, order='expiry_date asc, id asc', limit=1)

    def action_withdraw(self):
        self._check_manager()
        for batch in self:
            if batch.qty_available > 0:
                self.env['sf.pharmacy.batch_movement'].create({
                    'batch_id': batch.id,
                    'movement_type': 'withdrawal',
                    'qty': batch.qty_available,
                    'reference': 'Expiry withdrawal %s' % batch.name,
                    'company_id': batch.company_id.id,
                })
        return True

    def action_recall(self):
        self._check_manager()
        act_type = self.env.ref('mail.mail_activity_data_todo')
        for batch in self:
            if batch.qty_available > 0:
                self.env['sf.pharmacy.batch_movement'].create({
                    'batch_id': batch.id,
                    'movement_type': 'recall',
                    'qty': batch.qty_available,
                    'reference': 'Batch recall %s' % batch.name,
                    'company_id': batch.company_id.id,
                })
            dispensations = self.env['sf.pharmacy.dispensation'].search([
                ('batch_id', '=', batch.id),
                ('state', '=', 'done'),
            ])
            for disp in dispensations:
                user_id = disp.dispensed_by.id or disp.prescription_id.create_uid.id or self.env.uid
                subject = 'Batch recall %s - patient %s' % (batch.name, disp.prescription_id.patient_name)
                existing = self.env['mail.activity'].search([
                    ('activity_type_id', '=', act_type.id),
                    ('res_model', '=', batch._name),
                    ('res_id', '=', batch.id),
                    ('summary', '=', subject),
                    ('state', '!=', 'done'),
                ], limit=1)
                if not existing:
                    batch.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=subject,
                        note='Batch recall %s for dispensation %s' % (batch.name, disp.name),
                        user_id=user_id,
                    )
        return True

    @api.model
    def _schedule_todo(self, record, subject):
        act_type = self.env.ref('mail.mail_activity_data_todo')
        existing = self.env['mail.activity'].search([
            ('activity_type_id', '=', act_type.id),
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('summary', '=', subject),
            ('state', '!=', 'done'),
        ], limit=1)
        if existing:
            return True
        user_id = record.product_id.responsible_id.id or self.env.uid
        record.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=subject,
            note=subject,
            user_id=user_id,
        )
        return True

    @api.model
    def _cron_stock_alerts(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            batch_model = self.with_company(company)
            today = fields.Date.context_today(batch_model)
            icp = self.env['ir.config_parameter'].sudo()
            expiry_days = int(icp.get_param('sf_pharmacy.expiry_days', default='90'))
            low_stock = float(icp.get_param('sf_pharmacy.low_stock_threshold', default='5.0'))
            alert_date = today + timedelta(days=expiry_days)
            batches = self.env['sf.pharmacy.batch'].search([('company_id', '=', company.id)])
            for batch in batches:
                if batch.status == 'withdrawn':
                    continue
                if batch.expiry_date and batch.expiry_date <= alert_date:
                    subject = 'Expiry near or reached: %s' % batch.name
                    self._schedule_todo(batch, subject)
                if batch.qty_available <= low_stock:
                    subject = 'Low stock: %s' % batch.name
                    self._schedule_todo(batch, subject)
        return True
