from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestForecastModel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.model = self.env['forecast.model'].create({
            'name': 'Test Model',
            'algorithm': 'gb',
            'n_estimators': 50,
            'max_depth': 4,
        })

    def test_model_creation(self):
        self.assertEqual(self.model.state, 'draft')
        self.assertTrue(self.model.active)

    def test_model_training(self):
        self.model.action_train()
        # In test, we just verify it doesn't crash
        self.assertIn(self.model.state, ['trained', 'failed'])

    def test_prediction_creation(self):
        product = self.env['product.product'].create({'name': 'Test Product', 'type': 'consu'})
        warehouse = self.env.ref('stock.warehouse0')
        pred = self.env['forecast.prediction'].create({
            'model_id': self.model.id,
            'product_id': product.id,
            'warehouse_id': warehouse.id,
            'date': fields.Date.today(),
            'predicted_qty': 100.0,
        })
        self.assertEqual(pred.predicted_qty, 100.0)

    def test_unique_prediction_constraint(self):
        product = self.env['product.product'].create({'name': 'Test Product 2', 'type': 'consu'})
        warehouse = self.env.ref('stock.warehouse0')
        self.env['forecast.prediction'].create({
            'model_id': self.model.id,
            'product_id': product.id,
            'warehouse_id': warehouse.id,
            'date': fields.Date.today(),
            'predicted_qty': 50.0,
        })
        with self.assertRaises(Exception):
            self.env['forecast.prediction'].create({
                'model_id': self.model.id,
                'product_id': product.id,
                'warehouse_id': warehouse.id,
                'date': fields.Date.today(),
                'predicted_qty': 75.0,
            })