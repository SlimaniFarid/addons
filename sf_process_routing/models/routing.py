# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval


class ProcessRouting(models.Model):
    _name = 'sf.process.routing'
    _description = 'Process Routing'
    _rec_name = 'display_name'
    _order = 'product_id, sequence'

    display_name = fields.Char(string='Routing Name', compute='_compute_display_name', store=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    version_ids = fields.One2many('sf.process.routing.version', 'routing_id', string='Versions')
    active_version_id = fields.Many2one('sf.process.routing.version', string='Active Version',
                                        compute='_compute_active_version', store=True)
    is_default = fields.Boolean(string='Default Routing', default=False)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('product_code_uniq', 'unique(product_id, code)', 'Routing code must be unique per product.'),
    ]

    @api.depends('product_id', 'code', 'sequence')
    def _compute_display_name(self):
        for r in self:
            r.display_name = f"{r.product_id.default_code or r.product_id.name} - {r.code}"

    @api.depends('version_ids', 'version_ids.state', 'version_ids.effective_date')
    def _compute_active_version(self):
        today = fields.Date.today()
        for r in self:
            active = r.version_ids.filtered(
                lambda v: v.state == 'active' and v.effective_date <= today
            ).sorted(key=lambda v: v.effective_date, reverse=True)
            r.active_version_id = active[:1].id if active else False

    def select_best_routing(self, quantity=1.0, context=None):
        """Select the best routing based on conditions."""
        self.ensure_one()
        if not self.active_version_id:
            return None
        return self.active_version_id.select_best_route(quantity, context)

    @api.constrains('is_default', 'product_id', 'active')
    def _check_single_default(self):
        for r in self:
            if r.is_default and r.active:
                others = self.search([
                    ('product_id', '=', r.product_id.id),
                    ('is_default', '=', True),
                    ('active', '=', True),
                    ('id', '!=', r.id),
                ])
                if others:
                    raise models.ValidationError(_('Only one default routing allowed per product.'))


class ProcessRoutingVersion(models.Model):
    _name = 'sf.process.routing.version'
    _description = 'Process Routing Version'
    _rec_name = 'display_name'
    _order = 'effective_date desc'

    display_name = fields.Char(string='Version Name', compute='_compute_display_name', store=True)
    routing_id = fields.Many2one('sf.process.routing', string='Routing', required=True, ondelete='cascade')
    version = fields.Char(string='Version', required=True)
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today)
    expiry_date = fields.Date(string='Expiry Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('obsolete', 'Obsolete'),
    ], string='Status', default='draft')
    route_ids = fields.One2many('sf.process.route', 'version_id', string='Routes')
    condition_ids = fields.One2many('sf.process.routing.condition', 'version_id', string='Selection Conditions')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('routing_version_uniq', 'unique(routing_id, version)', 'Version must be unique per routing.'),
    ]

    @api.depends('routing_id', 'version')
    def _compute_display_name(self):
        for v in self:
            v.display_name = f"{v.routing_id.display_name} v{v.version}"

    def action_activate(self):
        self.write({'state': 'active'})
        # Deactivate other versions
        others = self.search([
            ('routing_id', '=', self.routing_id.id),
            ('id', '!=', self.id),
            ('state', '=', 'active'),
        ])
        others.write({'state': 'obsolete'})

    def action_obsolete(self):
        self.write({'state': 'obsolete'})

    def select_best_route(self, quantity=1.0, context=None):
        """Evaluate conditions and return the best route."""
        self.ensure_one()
        if not self.route_ids:
            return None
        context = context or {}
        context.update({'quantity': quantity, 'routing_version': self})
        
        # Evaluate each route's conditions
        best_route = None
        best_score = -1
        for route in self.route_ids.filtered(lambda r: r.active):
            score = route.evaluate_conditions(context)
            if score > best_score:
                best_score = score
                best_route = route
        return best_route


class ProcessRoute(models.Model):
    _name = 'sf.process.route'
    _description = 'Process Route'
    _order = 'sequence, priority'

    version_id = fields.Many2one('sf.process.routing.version', string='Routing Version', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    priority = fields.Integer(string='Priority', default=50, help='Higher = preferred when conditions equal')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    bom_id = fields.Many2one('mrp.bom', string='Bill of Materials', required=True)
    workcenter_ids = fields.Many2many('mrp.workcenter', string='Workcenters')
    estimated_time = fields.Float(string='Estimated Time (hours)')
    estimated_cost = fields.Float(string='Estimated Cost')
    condition_ids = fields.One2many('sf.process.routing.condition', 'route_id', string='Conditions')
    active = fields.Boolean(string='Active', default=True)

    def evaluate_conditions(self, context):
        """Evaluate all conditions and return a score."""
        if not self.condition_ids:
            return 100  # No conditions = always valid
        
        total_weight = sum(c.weight for c in self.condition_ids)
        if total_weight == 0:
            return 100
        
        score = 0
        for condition in self.condition_ids:
            if condition.evaluate(context):
                score += condition.weight
        return (score / total_weight) * 100


class ProcessRoutingCondition(models.Model):
    _name = 'sf.process.routing.condition'
    _description = 'Process Routing Condition'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    version_id = fields.Many2one('sf.process.routing.version', string='Routing Version', ondelete='cascade')
    route_id = fields.Many2one('sf.process.route', string='Route', ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    condition_type = fields.Selection([
        ('workcenter_load', 'Workcenter Load %'),
        ('workcenter_availability', 'Workcenter Available'),
        ('quality_score', 'Workcenter Quality Score'),
        ('lead_time', 'Route Lead Time'),
        ('cost', 'Route Cost'),
        ('capacity', 'Available Capacity'),
        ('custom', 'Custom Python Expression'),
    ], string='Condition Type', required=True)
    operator = fields.Selection([
        ('<', 'Less Than'),
        ('<=', 'Less or Equal'),
        ('>', 'Greater Than'),
        ('>=', 'Greater or Equal'),
        ('==', 'Equal'),
        ('!=', 'Not Equal'),
    ], string='Operator', default='<=')
    threshold = fields.Float(string='Threshold Value')
    weight = fields.Float(string='Weight', default=1.0)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')
    python_code = fields.Text(string='Python Expression', help='Available: context, route, workcenter')

    def evaluate(self, context):
        """Evaluate condition against context."""
        self.ensure_one()
        
        if self.condition_type == 'custom':
            try:
                local_dict = {'context': context, 'route': self.route_id, 'workcenter': self.workcenter_id}
                safe_eval(self.python_code, local_dict, mode="exec", nocopy=True)
                return bool(local_dict.get('result', False))
            except Exception:
                return False
        
        # Get the value to compare
        value = self._get_value(context)
        if value is None:
            return False
        
        # Apply operator
        if self.operator == '<':
            return value < self.threshold
        elif self.operator == '<=':
            return value <= self.threshold
        elif self.operator == '>':
            return value > self.threshold
        elif self.operator == '>=':
            return value >= self.threshold
        elif self.operator == '==':
            return value == self.threshold
        elif self.operator == '!=':
            return value != self.threshold
        return False

    def _get_value(self, context):
        """Get the value based on condition type."""
        wc = self.workcenter_id or (self.route_id.workcenter_ids[:1] if self.route_id.workcenter_ids else None)
        
        if self.condition_type == 'workcenter_load' and wc:
            # Simplified: would integrate with actual capacity planning
            return wc.capacity * 0.7  # placeholder
        
        elif self.condition_type == 'workcenter_availability' and wc:
            return 1.0 if wc.active else 0.0
        
        elif self.condition_type == 'quality_score' and wc:
            # Would integrate with quality module
            return 95.0  # placeholder
        
        elif self.condition_type == 'lead_time':
            return self.route_id.estimated_time or 0.0
        
        elif self.condition_type == 'cost':
            return self.route_id.estimated_cost or 0.0
        
        elif self.condition_type == 'capacity' and wc:
            return wc.capacity or 0.0
        
        return None


class RoutingSelectionLog(models.Model):
    _name = 'sf.process.routing.selection.log'
    _description = 'Routing Selection Log'
    _order = 'create_date desc'

    mo_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True, ondelete='cascade')
    routing_id = fields.Many2one('sf.process.routing', string='Routing', required=True)
    version_id = fields.Many2one('sf.process.routing.version', string='Version')
    route_id = fields.Many2one('sf.process.route', string='Selected Route')
    selection_method = fields.Selection([
        ('auto', 'Automatic'),
        ('manual', 'Manual Override'),
    ], string='Method', default='auto')
    score = fields.Float(string='Selection Score')
    user_id = fields.Many2one('res.users', string='Selected By', default=lambda self: self.env.user)
    create_date = fields.Datetime(string='Date', readonly=True)
    notes = fields.Text(string='Notes')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.process.routing'

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

