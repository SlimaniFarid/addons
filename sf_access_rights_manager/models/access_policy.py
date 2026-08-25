from odoo import api, fields, models
from odoo.exceptions import UserError


class AccessPolicy(models.Model):
    _name = 'access.policy'
    _description = 'Access Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'

    name = fields.Char(string='Policy Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Applied'),
        ('error', 'Error'),
    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)

    group_ids = fields.Many2many('res.groups', string='Applied To Groups', required=True,
        help='Users in these groups will have this policy applied.')
    company_ids = fields.Many2many('res.company', string='Companies',
        help='Limit to specific companies. Empty = all companies.')

    menu_rule_ids = fields.One2many('access.rule.menu', 'policy_id', string='Menu Rules')
    field_rule_ids = fields.One2many('access.rule.field', 'policy_id', string='Field Rules')
    action_rule_ids = fields.One2many('access.rule.action', 'policy_id', string='Action/Report Rules')
    export_rule_ids = fields.One2many('access.rule.export', 'policy_id', string='Export Rules')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Policy code must be unique.'),
    ]

    def action_apply(self):
        for pol in self:
            pol._apply_menu_rules()
            pol._apply_field_rules()
            pol._apply_action_rules()
            pol._apply_export_rules()
            pol.state = 'active'

    def action_reset(self):
        for pol in self:
            pol.state = 'draft'
            # Note: Full rollback would require storing previous state
            # This is a simplified implementation

    def _apply_menu_rules(self):
        Menu = self.env['ir.ui.menu']
        for rule in self.menu_rule_ids:
            menus = Menu.search([('id', 'in', rule.menu_ids.ids)])
            for menu in menus:
                groups = list(menu.groups_id.ids)
                if rule.action == 'hide':
                    # Add groups to hide from (menu visible only to OTHER groups)
                    # Odoo: if groups_id set, ONLY those groups see it
                    # To HIDE from specific groups, we need a different approach
                    # Simplified: set groups_id to groups that SHOULD see it
                    pass
                elif rule.action == 'show':
                    menu.write({'groups_id': [(4, g.id) for g in rule.group_ids]})

    def _apply_field_rules(self):
        # Field-level: create view inheritances with modifiers
        # This is a simplified implementation that creates view modifiers
        View = self.env['ir.ui.view']
        for rule in self.field_rule_ids:
            if not rule.model_id or not rule.field_id:
                continue
            # Find form views for the model
            views = View.search([
                ('model', '=', rule.model_id.model),
                ('type', '=', 'form'),
                ('mode', '=', 'primary'),
            ])
            for view in views:
                # Create an inheritance view with the modifier
                arch = f"""
                <xpath expr="//field[@name='{rule.field_id.name}']" position="attributes">
                    <attribute name="invisible">{1 if rule.action == 'invisible' else 0}</attribute>
                    <attribute name="readonly">{1 if rule.action == 'readonly' else 0}</attribute>
                    <attribute name="required">{1 if rule.action == 'required' else 0}</attribute>
                </xpath>
                """
                View.create({
                    'name': f'{view.name} - {rule.policy_id.code} - {rule.field_id.name}',
                    'model': rule.model_id.model,
                    'inherit_id': view.id,
                    'arch': arch,
                    'groups_id': [(6, 0, rule.group_ids.ids)],
                })

    def _apply_action_rules(self):
        Action = self.env['ir.actions.act_window']
        for rule in self.action_rule_ids:
            actions = Action.search([('id', 'in', rule.action_ids.ids)])
            for action in actions:
                if rule.action == 'deny':
                    action.write({'groups_id': [(4, g.id) for g in rule.group_ids]})
                elif rule.action == 'allow':
                    # Allow: remove any denying groups or ensure access
                    # By default Odoo allows access; 'allow' is a no-op for standard behavior
                    pass

    def _apply_export_rules(self):
        # Export control: add/remove 'Export' permission via groups on model
        # Find the export action for each model and adjust its groups
        Action = self.env['ir.actions.act_window']
        for rule in self.export_rule_ids:
            if not rule.model_id:
                continue
            # Find export actions for this model
            export_actions = Action.search([
                ('res_model', '=', rule.model_id.model),
                ('name', 'ilike', 'export'),
            ])
            for action in export_actions:
                if rule.action == 'deny':
                    action.write({'groups_id': [(4, g.id) for g in rule.group_ids]})
                elif rule.action == 'allow':
                    # Allow: ensure the groups have access
                    pass


class AccessRuleMenu(models.Model):
    _name = 'access.rule.menu'
    _description = 'Menu Access Rule'
    _order = 'sequence'

    policy_id = fields.Many2one('access.policy', string='Policy', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    action = fields.Selection([
        ('hide', 'Hide from Groups'),
        ('show', 'Show Only to Groups'),
    ], string='Action', required=True, default='hide')
    menu_ids = fields.Many2many('ir.ui.menu', string='Menus', required=True)
    group_ids = fields.Many2many('res.groups', string='Target Groups', required=True)
    description = fields.Char(string='Description')


class AccessRuleField(models.Model):
    _name = 'access.rule.field'
    _description = 'Field Access Rule'
    _order = 'sequence'

    policy_id = fields.Many2one('access.policy', string='Policy', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    model_id = fields.Many2one('ir.model', string='Model', required=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', required=True,
        domain="[('model_id', '=', model_id)]")
    action = fields.Selection([
        ('readonly', 'Read Only'),
        ('invisible', 'Invisible'),
        ('required', 'Required'),
    ], string='Action', required=True, default='readonly')
    group_ids = fields.Many2many('res.groups', string='Target Groups', required=True)
    condition = fields.Char(string='Domain Condition',
        help='Optional domain on the record (e.g. "[(\"state\", \"=\", \"done\")]")')

    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.field_id = False


class AccessRuleAction(models.Model):
    _name = 'access.rule.action'
    _description = 'Action/Report Access Rule'
    _order = 'sequence'

    policy_id = fields.Many2one('access.policy', string='Policy', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    action = fields.Selection([
        ('deny', 'Deny Access'),
        ('allow', 'Allow Access'),
    ], string='Action', required=True, default='deny')
    action_ids = fields.Many2many('ir.actions.actions', string='Actions/Reports', required=True)
    group_ids = fields.Many2many('res.groups', string='Target Groups', required=True)


class AccessRuleExport(models.Model):
    _name = 'access.rule.export'
    _description = 'Export Access Rule'
    _order = 'sequence'

    policy_id = fields.Many2one('access.policy', string='Policy', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    model_id = fields.Many2one('ir.model', string='Model', required=True)
    action = fields.Selection([
        ('deny', 'Deny Export'),
        ('allow', 'Allow Export'),
    ], string='Action', required=True, default='deny')
    group_ids = fields.Many2many('res.groups', string='Target Groups', required=True)
    field_ids = fields.Many2many('ir.model.fields', string='Allowed Fields (if allow)',
        domain="[('model_id', '=', model_id)]")