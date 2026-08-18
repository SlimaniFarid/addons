{
    'name': 'AI Demand Forecasting',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'ML-powered demand forecasting for inventory optimization',
    'description': """AI Demand Forecasting
======================

Replace static min/max rules with machine learning predictions.

Features:
- Automatic model training on historical sales, stock moves, promotions, seasonality
- Per-warehouse, per-product forecasts with confidence intervals
- Weather & holiday integration (optional)
- Replenishment recommendations with service level targets
- Model performance dashboard (MAE, MAPE, bias)
- No data science expertise required - fully automated

Technical:
- Uses scikit-learn (included) for Gradient Boosting / Random Forest
- Incremental retraining via cron
- Stores predictions in dedicated tables for reporting
- Compatible with Odoo's native procurement (orderpoint)""",
    'author': 'Ethan Miller',
    'support': 'tech@gmail.com',
    'license': 'OPL-1',
    'price': 299.0,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'sale'],
    'depends_optional': ['purchase', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/forecast_menus.xml',
        'views/forecast_model_views.xml',
        'views/forecast_prediction_views.xml',
        'views/forecast_config_views.xml',
        'data/forecast_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}

