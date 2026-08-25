from odoo.tests import TransactionCase

class TestAccessRights(TransactionCase):

    def setUp(self):
        super().setUp()
        self.group_sales = self.env.ref('sales_team.group_sale_salesman')
        self.group_account = self.env.ref('account.group_account_invoice')

    def test_policy_creation(self):
        policy = self.env['access.policy'].create({
            'name': 'Sales Restrictions',
            'code': 'SALES-RES',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        self.assertEqual(policy.state, 'draft')
        self.assertTrue(policy.active)

    def test_menu_rule_creation(self):
        policy = self.env['access.policy'].create({
            'name': 'Test Policy',
            'code': 'TEST-001',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        menu = self.env['ir.ui.menu'].search([('name', '=', 'Sales')], limit=1)
        rule = self.env['access.rule.menu'].create({
            'policy_id': policy.id,
            'action': 'hide',
            'menu_ids': [(6, 0, [menu.id])] if menu else [],
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        self.assertEqual(rule.action, 'hide')

    def test_field_rule_creation(self):
        policy = self.env['access.policy'].create({
            'name': 'Test Policy 2',
            'code': 'TEST-002',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        model = self.env['ir.model']._get('sale.order')
        field = self.env['ir.model.fields'].search([
            ('model_id', '=', model.id), ('name', '=', 'amount_untaxed')
        ], limit=1)
        rule = self.env['access.rule.field'].create({
            'policy_id': policy.id,
            'model_id': model.id,
            'field_id': field.id,
            'action': 'readonly',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        self.assertEqual(rule.action, 'readonly')

    def test_field_rule_application(self):
        """Test that field rule creates view inheritance"""
        policy = self.env['access.policy'].create({
            'name': 'Test Field Application',
            'code': 'TST-FLD',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        model = self.env['ir.model']._get('sale.order')
        field = self.env['ir.model.fields'].search([
            ('model_id', '=', model.id), ('name', '=', 'amount_untaxed')
        ], limit=1)
        self.env['access.rule.field'].create({
            'policy_id': policy.id,
            'model_id': model.id,
            'field_id': field.id,
            'action': 'readonly',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        policy.action_apply()
        # Check that view inheritance was created
        views = self.env['ir.ui.view'].search([
            ('model', '=', 'sale.order'),
            ('inherit_id', '!=', False),
        ])
        self.assertTrue(views.filtered(lambda v: 'amount_untaxed' in v.arch or 'readonly' in v.arch))

    def test_action_rule_application(self):
        """Test that action rule modifies action groups"""
        policy = self.env['access.policy'].create({
            'name': 'Test Action Application',
            'code': 'TST-ACT',
            'group_ids': [(6, 0, [self.group_sales.id])],
        })
        action = self.env['ir.actions.act_window'].search([
            ('res_model', '=', 'sale.order'), ('name', 'ilike', 'order')
        ], limit=1)
        if action:
            self.env['access.rule.action'].create({
                'policy_id': policy.id,
                'action': 'deny',
                'action_ids': [(6, 0, [action.id])],
                'group_ids': [(6, 0, [self.group_sales.id])],
            })
            policy.action_apply()
            action.refresh()
            self.assertIn(self.group_sales, action.groups_id)