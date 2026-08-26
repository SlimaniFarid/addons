# -*- coding: utf-8 -*-
"""SPC Models - Statistical Process Control Charts per AIAG SPC 2nd Edition."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import math
import statistics
import json
from dateutil.relativedelta import relativedelta


class IATFSPCChart(models.Model):
    """SPC Control Chart - X-bar/R, X-bar/S, I-MR, p, np, c, u."""
    _name = 'iatf.spc.chart'
    _description = 'SPC Control Chart'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Chart Name', required=True, tracking=True)
    chart_number = fields.Char(string='Chart Number', required=True, copy=False, readonly=True, default='New')
    # What is monitored
    product_id = fields.Many2one('product.product', string='Product', required=True)
    characteristic_name = fields.Char(string='Characteristic Name', required=True)
    characteristic_type = fields.Selection([
        ('variable', 'Variable (Measurement)'),
        ('attribute', 'Attribute (Count)'),
    ], string='Characteristic Type', required=True, default='variable')
    # Specification
    spec_usl = fields.Float(string='USL (Upper Spec Limit)')
    spec_lsl = fields.Float(string='LSL (Lower Spec Limit)')
    spec_target = fields.Float(string='Target / Nominal')
    # Chart type
    chart_type = fields.Selection([
        ('xbar_r', 'X-bar / R (Subgroups n=2-10)'),
        ('xbar_s', 'X-bar / S (Subgroups n>10)'),
        ('imr', 'Individuals / Moving Range (n=1)'),
        ('p', 'p-Chart (Fraction Defective)'),
        ('np', 'np-Chart (Number Defective)'),
        ('c', 'c-Chart (Defect Count)'),
        ('u', 'u-Chart (Defects per Unit)'),
    ], string='Chart Type', required=True, default='xbar_r')
    # Subgroup settings
    subgroup_size = fields.Integer(string='Subgroup Size (n)', default=5,
                                   help='Number of samples per subgroup (2-10 for X-bar/R, >10 for X-bar/S, 1 for I-MR)')
    frequency = fields.Selection([
        ('hourly', 'Hourly'),
        ('shift', 'Per Shift'),
        ('daily', 'Daily'),
        ('lot', 'Per Lot'),
        ('custom', 'Custom'),
    ], string='Sampling Frequency', default='hourly')
    # Control Limits (calculated or manual)
    ucl = fields.Float(string='UCL (Upper Control Limit)', readonly=True)
    lcl = fields.Float(string='LCL (Lower Control Limit)', readonly=True)
    cl = fields.Float(string='CL (Center Line)', readonly=True)
    # For attribute charts
    ucl_attr = fields.Float(string='UCL', readonly=True)
    lcl_attr = fields.Float(string='LCL', readonly=True)
    cl_attr = fields.Float(string='CL', readonly=True)
    # Capability (for variable charts)
    cp = fields.Float(string='Cp', readonly=True)
    cpk = fields.Float(string='Cpk', readonly=True)
    pp = fields.Float(string='Pp', readonly=True)
    ppk = fields.Float(string='Ppk', readonly=True)
    # Measurements
    measurement_ids = fields.One2many('iatf.spc.measurement', 'chart_id', string='Measurements')
    alert_ids = fields.One2many('iatf.spc.alert', 'chart_id', string='Alerts / Out-of-Control Signals')
    # Equipment / IoT
    equipment_id = fields.Many2one('maintenance.equipment', string='Measurement Equipment')
    iot_enabled = fields.Boolean(string='IoT Enabled', default=False,
                                 help='Accept measurements via MQTT/HTTP endpoint')
    iot_topic = fields.Char(string='MQTT Topic', help='Topic for IoT data ingestion')
    # Linked Control Plan line
    cp_line_id = fields.Many2one('iatf.control.plan.line', string='Control Plan Line', ondelete='restrict')
    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('chart_number', 'New') == 'New':
                vals['chart_number'] = self.env['ir.sequence'].next_by_code('iatf.spc.chart') or 'SPC-%s' % self.env['ir.sequence'].next_by_code('iatf.spc.chart')
        return super().create(vals_list)

    def action_calculate_limits(self):
        """Calculate control limits from measurement data."""
        for chart in self:
            chart._calculate_control_limits()
            chart._calculate_capability()

    def action_check_rules(self):
        """Check Western Electric / Nelson rules on latest measurements."""
        for chart in self:
            chart._check_western_electric_rules()

    def _calculate_control_limits(self):
        """Calculate control limits based on chart type and data."""
        self.ensure_one()
        measurements = self.measurement_ids.sorted('datetime')
        if not measurements:
            return

        if self.chart_type in ('xbar_r', 'xbar_s'):
            self._calc_xbar_r_s(measurements)
        elif self.chart_type == 'imr':
            self._calc_imr(measurements)
        elif self.chart_type in ('p', 'np', 'c', 'u'):
            self._calc_attribute(measurements)

    def _calc_xbar_r_s(self, measurements):
        """Calculate X-bar/R or X-bar/S limits."""
        subgroups = {}
        for m in measurements:
            sg = m.subgroup_index
            if sg not in subgroups:
                subgroups[sg] = []
            subgroups[sg].append(m.value)

        if not subgroups:
            return

        xbar_vals = []
        range_vals = []
        std_vals = []

        for sg, vals in subgroups.items():
            if len(vals) >= 2:
                xbar_vals.append(statistics.mean(vals))
                range_vals.append(max(vals) - min(vals))
                if len(vals) > 2:
                    std_vals.append(statistics.stdev(vals))

        if not xbar_vals:
            return

        cl = statistics.mean(xbar_vals)
        self.cl = cl

        # Control chart constants (AIAG SPC)
        n = self.subgroup_size
        constants = {
            2: {'A2': 1.880, 'D3': 0, 'D4': 3.267, 'B3': 0, 'B4': 3.267},
            3: {'A2': 1.023, 'D3': 0, 'D4': 2.575, 'B3': 0, 'B4': 2.568},
            4: {'A2': 0.729, 'D3': 0, 'D4': 2.282, 'B3': 0, 'B4': 2.266},
            5: {'A2': 0.577, 'D3': 0, 'D4': 2.115, 'B3': 0, 'B4': 2.089},
            6: {'A2': 0.483, 'D3': 0, 'D4': 2.004, 'B3': 0.030, 'B4': 1.970},
            7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924, 'B3': 0.118, 'B4': 1.882},
            8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864, 'B3': 0.185, 'B4': 1.815},
            9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816, 'B3': 0.239, 'B4': 1.761},
            10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777, 'B3': 0.284, 'B4': 1.716},
        }
        c = constants.get(n, constants[5])

        if self.chart_type == 'xbar_r' and range_vals:
            r_bar = statistics.mean(range_vals)
            self.ucl = cl + c['A2'] * r_bar
            self.lcl = cl - c['A2'] * r_bar
        elif self.chart_type == 'xbar_s' and std_vals:
            s_bar = statistics.mean(std_vals)
            self.ucl = cl + c['A3'] * s_bar if 'A3' in c else cl + 3 * s_bar / math.sqrt(n)
            self.lcl = cl - c['A3'] * s_bar if 'A3' in c else cl - 3 * s_bar / math.sqrt(n)

    def _calc_imr(self, measurements):
        """Calculate Individuals / Moving Range limits."""
        vals = [m.value for m in measurements]
        if len(vals) < 2:
            return

        cl = statistics.mean(vals)
        self.cl = cl

        # Moving ranges
        mr_vals = [abs(vals[i] - vals[i-1]) for i in range(1, len(vals))]
        mr_bar = statistics.mean(mr_vals)

        # Constants for n=2 (moving range of 2)
        self.ucl = cl + 2.66 * mr_bar
        self.lcl = cl - 2.66 * mr_bar

    def _calc_attribute(self, measurements):
        """Calculate attribute chart limits (p, np, c, u)."""
        # Placeholder - similar structure
        pass

    def _calculate_capability(self):
        """Calculate Cp, Cpk, Pp, Ppk for variable charts."""
        self.ensure_one()
        if self.chart_type not in ('xbar_r', 'xbar_s', 'imr'):
            return
        if not (self.spec_usl and self.spec_lsl):
            return

        measurements = self.measurement_ids
        vals = [m.value for m in measurements]
        if len(vals) < 2:
            return

        # Within-subgroup (short-term) for Cp/Cpk
        if self.chart_type in ('xbar_r', 'xbar_s'):
            subgroups = {}
            for m in measurements:
                sg = m.subgroup_index
                if sg not in subgroups:
                    subgroups[sg] = []
                subgroups[sg].append(m.value)

            within_std = 0
            count = 0
            for sg, v in subgroups.items():
                if len(v) >= 2:
                    within_std += statistics.stdev(v)
                    count += 1
            if count:
                within_std /= count
        else:
            # I-MR: use moving range
            mr_vals = [abs(vals[i] - vals[i-1]) for i in range(1, len(vals))]
            within_std = statistics.mean(mr_vals) / 1.128 if mr_vals else 0

        # Overall (long-term) for Pp/Ppk
        overall_std = statistics.stdev(vals) if len(vals) >= 2 else 0

        tolerance = self.spec_usl - self.spec_lsl

        if within_std > 0:
            self.cp = tolerance / (6 * within_std)
            cpu = (self.spec_usl - self.spec_target) / (3 * within_std) if self.spec_target else 0
            cpl = (self.spec_target - self.spec_lsl) / (3 * within_std) if self.spec_target else 0
            self.cpk = min(cpu, cpl) if cpu and cpl else 0

        if overall_std > 0:
            self.pp = tolerance / (6 * overall_std)
            cpu = (self.spec_usl - self.spec_target) / (3 * overall_std) if self.spec_target else 0
            cpl = (self.spec_target - self.spec_lsl) / (3 * overall_std) if self.spec_target else 0
            self.ppk = min(cpu, cpl) if cpu and cpl else 0

    def _check_western_electric_rules(self):
        """Check Western Electric / Nelson rules for out-of-control signals."""
        self.ensure_one()
        measurements = self.measurement_ids.sorted('datetime')
        if len(measurements) < 8:
            return

        vals = [m.value for m in measurements]
        cl = self.cl
        ucl = self.ucl
        lcl = self.lcl
        sigma = (ucl - cl) / 3 if ucl and cl else 0

        if sigma <= 0:
            return

        # Rule 1: Any point beyond 3σ (UCL/LCL)
        for i, m in enumerate(measurements):
            if m.value > ucl or m.value < lcl:
                self._create_alert(m, 1, f'Point beyond 3σ limit (value: {m.value})')

        # Rule 2: 2 of 3 consecutive points beyond 2σ on same side
        for i in range(len(measurements) - 2):
            pts = measurements[i:i+3]
            above_2sigma = sum(1 for m in pts if m.value > cl + 2*sigma)
            below_2sigma = sum(1 for m in pts if m.value < cl - 2*sigma)
            if above_2sigma >= 2 or below_2sigma >= 2:
                self._create_alert(pts[2], 2, f'2 of 3 points beyond 2σ on same side')

        # Rule 3: 4 of 5 consecutive points beyond 1σ on same side
        for i in range(len(measurements) - 4):
            pts = measurements[i:i+5]
            above_1sigma = sum(1 for m in pts if m.value > cl + sigma)
            below_1sigma = sum(1 for m in pts if m.value < cl - sigma)
            if above_1sigma >= 4 or below_1sigma >= 4:
                self._create_alert(pts[4], 3, f'4 of 5 points beyond 1σ on same side')

        # Rule 4: 8 consecutive points on same side of center line
        for i in range(len(measurements) - 7):
            pts = measurements[i:i+8]
            all_above = all(m.value > cl for m in pts)
            all_below = all(m.value < cl for m in pts)
            if all_above or all_below:
                self._create_alert(pts[7], 4, f'8 consecutive points on same side of CL')

    def _create_alert(self, measurement, rule_number, description):
        """Create SPC alert if not already exists."""
        existing = self.env['iatf.spc.alert'].search([
            ('chart_id', '=', self.id),
            ('measurement_id', '=', measurement.id),
            ('rule_number', '=', rule_number),
            ('state', 'in', ['new', 'acknowledged']),
        ])
        if not existing:
            self.env['iatf.spc.alert'].create({
                'chart_id': self.id,
                'measurement_id': measurement.id,
                'rule_number': rule_number,
                'description': description,
                'state': 'new',
            })

    def ingest_iot_measurement(self, value, subgroup_index=None, timestamp=None):
        """Endpoint for IoT sensor data ingestion."""
        self.ensure_one()
        if not self.iot_enabled:
            raise ValidationError(_('IoT ingestion not enabled for this chart.'))

        vals = {
            'chart_id': self.id,
            'value': value,
            'datetime': timestamp or fields.Datetime.now(),
            'subgroup_index': subgroup_index or 1,
        }
        measurement = self.env['iatf.spc.measurement'].create(vals)
        # Auto-check rules on new point
        self._check_western_electric_rules()
        return measurement


class IATFSPCMeasurement(models.Model):
    """Individual Measurement / Subgroup for SPC Chart."""
    _name = 'iatf.spc.measurement'
    _description = 'SPC Measurement'
    _order = 'datetime, subgroup_index, id'

    chart_id = fields.Many2one('iatf.spc.chart', string='SPC Chart', required=True, ondelete='cascade')
    datetime = fields.Datetime(string='Date/Time', required=True, default=fields.Datetime.now)
    subgroup_index = fields.Integer(string='Subgroup Index', default=1)
    value = fields.Float(string='Measured Value', required=True)
    # Computed for subgroup display
    subgroup_mean = fields.Float(string='Subgroup Mean', compute='_compute_subgroup_stats', store=True)
    subgroup_range = fields.Float(string='Subgroup Range', compute='_compute_subgroup_stats', store=True)
    subgroup_std = fields.Float(string='Subgroup Std Dev', compute='_compute_subgroup_stats', store=True)
    # Out-of-control rules triggered
    ooc_rules_triggered = fields.Json(string='OOC Rules Triggered', default=list)
    # Company
    company_id = fields.Many2one(related='chart_id.company_id', store=True)

    @api.depends('chart_id', 'subgroup_index', 'value')
    def _compute_subgroup_stats(self):
        for m in self:
            siblings = self.search([
                ('chart_id', '=', m.chart_id.id),
                ('subgroup_index', '=', m.subgroup_index),
            ])
            if len(siblings) >= 2:
                vals = siblings.mapped('value')
                m.subgroup_mean = statistics.mean(vals)
                m.subgroup_range = max(vals) - min(vals)
                m.subgroup_std = statistics.stdev(vals) if len(vals) > 2 else 0
            else:
                m.subgroup_mean = m.value
                m.subgroup_range = 0
                m.subgroup_std = 0


class IATFSPCAlert(models.Model):
    """SPC Alert - Out-of-Control Signal."""
    _name = 'iatf.spc.alert'
    _description = 'SPC Alert'
    _order = 'create_date desc'

    chart_id = fields.Many2one('iatf.spc.chart', string='SPC Chart', required=True, ondelete='cascade')
    measurement_id = fields.Many2one('iatf.spc.measurement', string='Measurement', required=True, ondelete='cascade')
    rule_number = fields.Integer(string='Rule Number', required=True,
                                 help='1=Beyond 3σ, 2=2 of 3 beyond 2σ, 3=4 of 5 beyond 1σ, 4=8 same side CL')
    description = fields.Char(string='Description', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ], string='State', default='new', tracking=True)
    acknowledged_by_id = fields.Many2one('res.users', string='Acknowledged By')
    acknowledged_date = fields.Datetime(string='Acknowledged Date')
    resolved_by_id = fields.Many2one('res.users', string='Resolved By')
    resolved_date = fields.Datetime(string='Resolved Date')
    resolution_notes = fields.Text(string='Resolution Notes')
    # Company
    company_id = fields.Many2one(related='chart_id.company_id', store=True)

    def action_acknowledge(self):
        self.write({
            'state': 'acknowledged',
            'acknowledged_by_id': self.env.uid,
            'acknowledged_date': fields.Datetime.now(),
        })

    def action_resolve(self):
        self.write({
            'state': 'resolved',
            'resolved_by_id': self.env.uid,
            'resolved_date': fields.Datetime.now(),
        })

    def action_false_alarm(self):
        self.write({'state': 'false_alarm'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'iatf.apqp.project'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
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
class _WaveFinalStock(models.Model):
    _inherit = 'iatf.apqp.project'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
