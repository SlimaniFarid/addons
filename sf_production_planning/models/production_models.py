# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ProductionPlan(models.Model):
    _name = 'sf.mps'
    _description = 'Master Production Schedule (MPS)'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    date_start = fields.Date(string='Start date', required=True)
    date_end = fields.Date(string='End date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True)
    line_ids = fields.One2many('sf.mps.line', 'mps_id',
                               string='Plan lines')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This plan number already exists.')),
        ('date_order', 'CHECK(date_end >= date_start)',
         _('The end date must be on or after the start date.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.mps')
            vals['name'] = 'MPS-%s' % seq
        return super().create(vals)

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft plans can be confirmed.'))
        self.state = 'confirmed'

    def action_close(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed plans can be closed.'))
        self.state = 'closed'

    def action_load_productions(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Productions can be loaded only while the '
                              'plan is a draft.'))
        return {
            'name': _('Load Manufacturing Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.mps.load.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mps_id': self.id},
        }

    def _check_workcenter_load(self):
        result = {}
        lines = self.line_ids.filtered(
            lambda l: l.state in ('planned', 'confirmed'))
        for line in lines:
            result.setdefault(line.workcenter_id, 0.0)
            result[line.workcenter_id] += line.duration_hours
        return result

    def unlink(self):
        for plan in self:
            if plan.state != 'draft':
                raise UserError(_('A confirmed or closed plan cannot be '
                                  'deleted.'))
        return super().unlink()


class ProductionPlanLine(models.Model):
    _name = 'sf.mps.line'
    _description = 'MPS Plan Line'
    _order = 'workcenter_id, date_start, priority'

    mps_id = fields.Many2one('sf.mps', string='Plan', required=True,
                             ondelete='cascade', index=True)
    workcenter_id = fields.Many2one('mrp.workcenter',
                                    string='Work center', required=True,
                                    index=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    production_id = fields.Many2one('mrp.production', string='MO',
                                    ondelete='set null')
    quantity = fields.Float(string='Quantity', required=True)
    date_start = fields.Datetime(string='Start', required=True, index=True)
    date_end = fields.Datetime(string='End', required=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal', required=True)
    duration_hours = fields.Float(string='Duration (hours)',
                                  default=1.0)
    state = fields.Selection([
        ('planned', 'Planned'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='planned', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='mps_id.company_id', store=True,
                                 readonly=True)

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)',
         _('The quantity must be positive.')),
        ('date_order', 'CHECK(date_end >= date_start)',
         _('The end date must be on or after the start date.')),
    ]

    @api.onchange('production_id', 'quantity')
    def _onchange_duration(self):
        if self.production_id:
            self.product_id = self.production_id.product_id
            self.quantity = self.production_id.product_qty
        self._compute_duration()

    def _compute_duration(self):
        for line in self:
            if line.production_id and line.workcenter_id:
                wc = line.workcenter_id
                line.duration_hours = wc.time_start + wc.time_stop + \
                    line.quantity * wc.time_efficiency
            elif line.quantity:
                line.duration_hours = line.quantity * 0.5

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line._compute_duration()
        return line

    def action_set_done(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed lines can be marked as done.'))
        self.state = 'done'

    def action_reopen_line(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only done lines can be reopened.'))
        self.state = 'confirmed'

    def unlink(self):
        for line in self:
            if line.state == 'confirmed':
                raise UserError(_('A confirmed line cannot be deleted. '
                                  'Mark it as done or reopen the plan.'))
        return super().unlink()


class MpsLoadWizard(models.TransientModel):
    _name = 'sf.mps.load.wizard'
    _description = 'Load Manufacturing Orders into MPS'

    mps_id = fields.Many2one('sf.mps', string='Plan', required=True)
    workcenter_id = fields.Many2one('mrp.workcenter',
                                    string='Default work center')
    production_ids = fields.Many2many('mrp.production',
                                      string='Manufacturing orders',
                                      domain="[('state', '=', 'draft')]")

    def action_load(self):
        self.ensure_one()
        if not self.production_ids:
            raise UserError(_('Select at least one manufacturing order.'))
        plan = self.mps_id
        now = fields.Datetime.now()
        lines = []
        for production in self.production_ids:
            workcenter = production.workorder_ids[:1].workcenter_id
            if not workcenter:
                workcenter = self.workcenter_id
            if not workcenter:
                raise UserError(_('MO %s has no work center and no default '
                                  'work center was set.')
                                % (production.name,))
            date_start = production.date_start or now
            line_vals = {
                'mps_id': plan.id,
                'workcenter_id': workcenter.id,
                'product_id': production.product_id.id,
                'production_id': production.id,
                'quantity': production.product_qty,
                'date_start': date_start,
                'priority': 'normal',
            }
            line = self.env['sf.mps.line'].create(line_vals)
            date_end = line.date_start + timedelta(
                hours=line.duration_hours)
            line.write({'date_end': date_end})
        return {'type': 'ir.actions.act_window_close'}