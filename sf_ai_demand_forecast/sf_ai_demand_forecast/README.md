# AI Demand Forecasting

ML-powered demand forecasting for inventory optimization

AI Demand Forecasting
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
- Compatible with Odoo's native procurement (orderpoint)
