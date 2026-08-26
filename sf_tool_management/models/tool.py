from datetime import timedelta

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Tool(models.Model):
    _name = 'sf.tool'
    _description = 'Tool / Gauge / Fixture'
    _rec_name = 'display_name'
    _order = 'code'

    display_name = fields.Char(string='Tool Name', compute='_compute_display_name', store=True)
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    tool_type = fields.Selection([
        ('cutting', 'Cutting Tool'),
        ('measuring', 'Measuring Instrument'),
        ('fixture', 'Fixture / Jig'),
        ('gage', 'Gage / Gauge'),
        ('hand', 'Hand Tool'),
        ('other', 'Other'),
    ], string='Type', required=True, default='cutting')
    category_id = fields.Many2one('sf.tool.category', string='Category')
    manufacturer = fields.Char(string='Manufacturer')
    model = fields.Char(string='Model')
    serial_number = fields.Char(string='Serial Number')
    specifications = fields.Text(string='Specifications')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    
    # Location & Assignment
    location_id = fields.Many2one('stock.location', string='Storage Location')
    workcenter_id = fields.Many2one('mrp.workcenter', string='Assigned Workcenter')
    current_holder_id = fields.Many2one('res.users', string='Current Holder')
    state = fields.Selection([
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('calibration', 'In Calibration'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
        ('lost', 'Lost'),
    ], string='Status', default='available', tracking=True)
    
    # Calibration
    calibration_required = fields.Boolean(string='Requires Calibration', default=True)
    calibration_frequency = fields.Integer(string='Calibration Frequency (days)', default=365)
    last_calibration_date = fields.Date(string='Last Calibration')
    next_calibration_date = fields.Date(string='Next Calibration Due', compute='_compute_next_calibration', store=True)
    calibration_certificate = fields.Binary(string='Calibration Certificate', attachment=True)
    calibration_cert_filename = fields.Char(string='Certificate Filename')
    calibration_status = fields.Selection([
        ('valid', 'Valid'),
        ('due_soon', 'Due Soon'),
        ('overdue', 'Overdue'),
        ('not_required', 'Not Required'),
    ], string='Calibration Status', compute='_compute_calibration_status', store=True)
    
    # Wear & Life
    max_wear = fields.Float(string='Max Wear Limit')
    current_wear = fields.Float(string='Current Wear', default=0.0)
    wear_unit = fields.Selection([
        ('hours', 'Hours'),
        ('parts', 'Parts Produced'),
        ('cycles', 'Cycles'),
        ('mm', 'Millimeters'),
        ('inches', 'Inches'),
    ], string='Wear Unit', default='hours')
    wear_alert_threshold = fields.Float(string='Wear Alert Threshold %', default=80.0)
    wear_status = fields.Selection([
        ('good', 'Good'),
        ('warning', 'Warning'),
        ('critical', 'Critical - Replace'),
    ], string='Wear Status', compute='_compute_wear_status', store=True)
    
    # Cost
    purchase_cost = fields.Float(string='Purchase Cost')
    purchase_date = fields.Date(string='Purchase Date')
    depreciation_method = fields.Selection([
        ('straight', 'Straight Line'),
        ('units', 'Units of Production'),
    ], string='Depreciation Method', default='straight')
    useful_life_years = fields.Integer(string='Useful Life (years)', default=5)
    residual_value = fields.Float(string='Residual Value', default=0.0)
    
    # Relations
    calibration_ids = fields.One2many('sf.tool.calibration', 'tool_id', string='Calibration History')
    wear_log_ids = fields.One2many('sf.tool.wear.log', 'tool_id', string='Wear Logs')
    assignment_ids = fields.One2many('sf.tool.assignment', 'tool_id', string='Assignments')
    maintenance_ids = fields.One2many('maintenance.request', 'tool_id', string='Maintenance Requests')
    
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Tool code must be unique.'),
    ]

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for t in self:
            t.display_name = f"[{t.code}] {t.name}"

    @api.depends('last_calibration_date', 'calibration_frequency', 'calibration_required')
    def _compute_next_calibration(self):
        for t in self:
            if t.calibration_required and t.last_calibration_date:
                t.next_calibration_date = t.last_calibration_date + timedelta(days=t.calibration_frequency)
            else:
                t.next_calibration_date = False

    @api.depends('next_calibration_date', 'calibration_required')
    def _compute_calibration_status(self):
        today = fields.Date.today()
        for t in self:
            if not t.calibration_required:
                t.calibration_status = 'not_required'
            elif not t.next_calibration_date:
                t.calibration_status = 'overdue'
            elif t.next_calibration_date <= today:
                t.calibration_status = 'overdue'
            elif t.next_calibration_date <= today + timedelta(days=30):
                t.calibration_status = 'due_soon'
            else:
                t.calibration_status = 'valid'

    @api.depends('current_wear', 'max_wear', 'wear_alert_threshold')
    def _compute_wear_status(self):
        for t in self:
            if t.max_wear and t.max_wear > 0:
                pct = (t.current_wear / t.max_wear) * 100
                if pct >= 100:
                    t.wear_status = 'critical'
                elif pct >= t.wear_alert_threshold:
                    t.wear_status = 'warning'
                else:
                    t.wear_status = 'good'
            else:
                t.wear_status = 'good'

    def action_assign(self):
        self.ensure_one()
        self.write({'state': 'assigned', 'current_holder_id': self.env.user.id})
        self.env['sf.tool.assignment'].create({
            'tool_id': self.id,
            'user_id': self.env.user.id,
            'assignment_date': fields.Date.today(),
            'state': 'assigned',
        })

    def action_return(self):
        self.ensure_one()
        self.write({'state': 'available', 'current_holder_id': False})
        assignment = self.env['sf.tool.assignment'].search([
            ('tool_id', '=', self.id),
            ('state', '=', 'assigned'),
        ], limit=1, order='assignment_date desc')
        if assignment:
            assignment.write({'state': 'returned', 'return_date': fields.Date.today()})

    def action_send_calibration(self):
        self.ensure_one()
        self.write({'state': 'calibration'})

    def action_receive_calibration(self, certificate=None):
        self.ensure_one()
        self.write({
            'state': 'available',
            'last_calibration_date': fields.Date.today(),
            'calibration_certificate': certificate,
        })
        self.env['sf.tool.calibration'].create({
            'tool_id': self.id,
            'calibration_date': fields.Date.today(),
            'certificate': certificate,
            'performed_by': self.env.user.id,
        })

    def log_wear(self, wear_increment, unit=None):
        self.ensure_one()
        unit = unit or self.wear_unit
        self.current_wear += wear_increment
        self.env['sf.tool.wear.log'].create({
            'tool_id': self.id,
            'date': fields.Date.today(),
            'wear_increment': wear_increment,
            'total_wear': self.current_wear,
            'unit': unit,
            'logged_by': self.env.user.id,
        })


class ToolCategory(models.Model):
    _name = 'sf.tool.category'
    _description = 'Tool Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    tool_ids = fields.One2many('sf.tool', 'category_id', string='Tools')


class ToolCalibration(models.Model):
    _name = 'sf.tool.calibration'
    _description = 'Tool Calibration Record'
    _order = 'calibration_date desc'

    tool_id = fields.Many2one('sf.tool', string='Tool', required=True, ondelete='cascade')
    calibration_date = fields.Date(string='Calibration Date', required=True, default=fields.Date.today)
    certificate = fields.Binary(string='Certificate', attachment=True)
    cert_filename = fields.Char(string='Certificate Filename')
    performed_by = fields.Many2one('res.users', string='Performed By', default=lambda self: self.env.user)
    lab_name = fields.Char(string='Calibration Lab')
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('conditional', 'Conditional Pass'),
    ], string='Result', default='pass')
    notes = fields.Text(string='Notes')
    next_due_date = fields.Date(string='Next Due Date')


class ToolWearLog(models.Model):
    _name = 'sf.tool.wear.log'
    _description = 'Tool Wear Log'
    _order = 'date desc'

    tool_id = fields.Many2one('sf.tool', string='Tool', required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    wear_increment = fields.Float(string='Wear Increment', required=True)
    total_wear = fields.Float(string='Total Wear After', required=True)
    unit = fields.Selection([
        ('hours', 'Hours'),
        ('parts', 'Parts Produced'),
        ('cycles', 'Cycles'),
        ('mm', 'Millimeters'),
        ('inches', 'Inches'),
    ], string='Unit', required=True)
    logged_by = fields.Many2one('res.users', string='Logged By', default=lambda self: self.env.user)
    notes = fields.Text(string='Notes')


class ToolAssignment(models.Model):
    _name = 'sf.tool.assignment'
    _description = 'Tool Assignment'
    _order = 'assignment_date desc'

    tool_id = fields.Many2one('sf.tool', string='Tool', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Assigned To', required=True)
    assigned_by = fields.Many2one('res.users', string='Assigned By', default=lambda self: self.env.user)
    assignment_date = fields.Date(string='Assignment Date', required=True, default=fields.Date.today)
    return_date = fields.Date(string='Return Date')
    expected_return_date = fields.Date(string='Expected Return')
    state = fields.Selection([
        ('assigned', 'Assigned'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], string='Status', default='assigned')
    location_id = fields.Many2one('stock.location', string='Usage Location')
    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')
    mo_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    notes = fields.Text(string='Notes')

    def action_return(self):
        self.write({'state': 'returned', 'return_date': fields.Date.today()})
        self.tool_id.action_return()


from datetime import timedelta

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.tool'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('next_due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.next_due_date
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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.tool'

    def action_refresh_business(self):
        """Pull active MO count and average yield."""
        Mos = self.env['mrp.production']
        active = Mos.search([('state', 'in', ('confirmed', 'progress'))])
        done = Mos.search([('state', '=', 'done')], limit=50)
        yields = [(mo.qty_produced / mo.product_qty * 100)
                  for mo in done if mo.product_qty]
        avg_yield = sum(yields) / len(yields) if yields else 0.0
        for rec in self:
            rec.message_post(body=_(
                '{a} active MO(s), avg yield {y:.1f}% on last {d} done.')
                .format(a=len(active), y=avg_yield, d=len(done)))
        return True
