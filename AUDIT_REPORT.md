# Audit Report - Odoo 18.0 Addons

**Date:** 25/08/2026
**Total Modules Audited:** 535

## Executive Summary

- **Modules with security issues (eval/exec):** 0
- **Total eval/exec occurrences:** 0
- **Modules with sudo() usage:** 33
- **Modules with empty methods (stubs):** 0
- **Total stub methods:** 0
- **Modules missing tests:** 392
- **AI modules without real implementation:** 29
- **Duplicate module groups detected:** 2348
- **__pycache__ files found:** 0

## Duplicate Modules Analysis

| Module 1 | Module 2 | Overall | Models | Files | Fields | Methods | Verdict |
|----------|----------|---------|--------|-------|--------|---------|---------|
| sf_accrual_reversal_auto | sf_bank_fee_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_accrual_reversal_auto | sf_capital_expenditure_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_accrual_reversal_auto | sf_currency_exposure_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_accrual_reversal_auto | sf_financial_ratio_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_batch_job_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_churn_prediction_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_compensation_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_competitive_intel_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_api_integration_log | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_bank_fee_analytics | sf_capital_expenditure_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_bank_fee_analytics | sf_currency_exposure_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_bank_fee_analytics | sf_financial_ratio_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_churn_prediction_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_compensation_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_competitive_intel_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_batch_job_monitor | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_business_requirement | sf_purchase_requisition_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_churn_prediction_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_compensation_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_competitive_intel_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capacity_planner | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capital_expenditure_plan | sf_currency_exposure_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_capital_expenditure_plan | sf_financial_ratio_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_change_freeze_calendar | sf_order_freeze_windows | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_compensation_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_competitive_intel_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_churn_prediction_rules | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_competitive_intel_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compensation_benchmark | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_escalation_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_competitive_intel_register | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_calendar | sf_compliance_obligation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_calendar | sf_customer_care_sla_breach | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_calendar | sf_employee_engagement_action | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_calendar | sf_sales_playbook | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_obligation | sf_customer_care_sla_breach | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_obligation | sf_employee_engagement_action | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_compliance_obligation | sf_sales_playbook | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_currency_exposure_map | sf_financial_ratio_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_advocacy_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_escalation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_escalation_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_journey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advisory_board | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_escalation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_escalation_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_journey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_advocacy_program | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_care_escalation_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_care_journey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_care_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_care_sla_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_dashboard | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_matrix | sf_customer_care_escalation_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_matrix | sf_quality_alert_escalation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_rules | sf_quality_alert_escalation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_care_journey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_care_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_escalation_tracker | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_care_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_journey | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_qa_review | sf_customer_care_qa_scorecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_care_satisfaction_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_care_sla | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_satisfaction_survey | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_churn_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_breach | sf_employee_engagement_action | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_breach | sf_sales_playbook | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_care_sla_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_dashboard | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_care_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_sla_rules | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_care_workforce | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_survey | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_disciplinary_action | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_employee_skill_gap | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_grievance_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_project_resource_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_training_plan | sf_customer_care_workload | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_care_workforce_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_customer_contract_renewal_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_care_workforce_plan | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_covenant_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_churn_analytics | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_customer_journey_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_forecast | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_pipeline | sf_customer_expansion_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_pipeline | sf_customer_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_contract_renewal_pipeline | sf_revenue_protection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_journey_map | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_covenant_tracker | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_expansion_tracker | sf_customer_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_expansion_tracker | sf_revenue_protection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_feedback_analytics | sf_fixed_asset_transfer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_feedback_analytics | sf_supplier_performance_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_health_scoring | sf_sales_commission_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_health_scoring | sf_supplier_risk_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_health_scoring | sf_telework_policy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_health_scoring | sf_upsell_trigger_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_customer_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_analytics | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_journey_mapper | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_map | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_journey_stage | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_mapper | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_journey_stage | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_checklist | sf_revenue_protection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_pain_point | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_onboarding_cost | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_customer_payment_behavior | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_pain_point | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_customer_payment_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_behavior | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_customer_profitability_rank | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_payment_plan | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_profitability_rank | sf_customer_reference_program | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_profitability_rank | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_profitability_rank | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_profitability_rank | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_profitability_rank | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_program | sf_customer_reference_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_program | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_program | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_program | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_tracker | sf_field_service_customer_satisfaction | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_tracker | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_reference_tracker | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_customer_satisfaction_trend | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_risk_score | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_customer_segments_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_satisfaction_trend | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_data_quality_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_customer_segments_rules | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_dr_plan_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_data_quality_check | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_deal_desk_request | sf_revenue_milestone | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_inventory_abc_classification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_inventory_count_variance | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_inventory_shrinkage_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_inventory_turnover_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_obsolescence_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_demand_planning_review | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_disciplinary_action | sf_employee_skill_gap | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_disciplinary_action | sf_grievance_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_disciplinary_action | sf_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_disciplinary_action | sf_project_resource_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_disciplinary_action | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_employee_survey | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_dr_plan_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_engagement_action | sf_sales_playbook | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_skill_gap | sf_grievance_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_skill_gap | sf_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_skill_gap | sf_project_resource_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_skill_gap | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_energy_saving_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_employee_survey | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_environmental_waste_tracking | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_energy_saving_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_intercompany_loan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_environmental_waste_tracking | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_equipment_utilization | sf_maintenance_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_equipment_utilization | sf_maintenance_schedule_optimizer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_field_service_customer_satisfaction | sf_revenue_leak_detector | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_field_service_customer_satisfaction | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_fixed_asset_transfer | sf_supplier_performance_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_grievance_tracker | sf_onboarding_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_grievance_tracker | sf_project_resource_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_grievance_tracker | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_inventory_accuracy_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_intercompany_loan | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_inventory_count_variance | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_inventory_shrinkage_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_inventory_turnover_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_obsolescence_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_abc_classification | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_marketing_budget_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_accuracy_rate | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_inventory_shrinkage_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_inventory_turnover_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_obsolescence_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_count_variance | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_revaluation | sf_policy_exception_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_inventory_turnover_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_obsolescence_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_shrinkage_tracker | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_obsolescence_forecast | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_inventory_turnover_analysis | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_maintenance_cost_tracker | sf_maintenance_schedule_optimizer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_marketing_campaign_roi | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_budget_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_nonconformance_cost | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_marketing_campaign_roi | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_production_capacity_whatif | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_nonconformance_cost | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_product_margin_matrix | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_obsolescence_forecast | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_onboarding_cost | sf_project_resource_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_onboarding_cost | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_purchase_contract_compliance | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_recurring_cost_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_audit_scheduler | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_capacity_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_procurement_savings_tracker | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_product_return_rate | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_margin_matrix | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_return_rate | sf_production_scrap_analytics | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_return_rate | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_return_rate | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_return_rate | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_product_return_rate | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_plan | sf_production_line_efficiency | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_plan | sf_production_oee_calculator | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_plan | sf_production_oee_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_production_downtime_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_capacity_whatif | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_production_oee_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_downtime_pareto | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_line_efficiency | sf_production_oee_calculator | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_line_efficiency | sf_production_oee_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_calculator | sf_production_oee_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_production_scrap_pareto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_oee_dashboard | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_priority | sf_production_order_sequencing | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_priority | sf_production_schedule_alert | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_priority | sf_production_waste_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_priority | sf_production_yield_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_sequencing | sf_production_schedule_alert | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_sequencing | sf_production_waste_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_order_sequencing | sf_production_yield_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_schedule_alert | sf_production_waste_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_schedule_alert | sf_production_yield_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_analytics | sf_quality_inspection_mobile2 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_analytics | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_analytics | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_analytics | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_project_lessons_learned | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_scrap_pareto | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_production_waste_tracker | sf_production_yield_analysis | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_charter | sf_project_portfolio_board | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_project_milestone_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_lessons_learned | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_project_stakeholder | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_milestone_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_resource_plan | sf_safety_training_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_quality_cost_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_project_stakeholder | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_recurring_cost_register | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_audit_scheduler | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_capacity_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_purchase_contract_compliance | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_quality_pareto_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_cost_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_document_control | sf_quality_document_control_sys | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_mobile2 | sf_quality_inspection_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_mobile2 | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_mobile2 | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_plan | sf_quality_inspection_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_plan | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_inspection_planner | sf_warehouse_slotting_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_quality_trend_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_pareto_analyzer | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_asset_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_quality_trend_dashboard | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_audit_scheduler | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_capacity_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_recurring_cost_register | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_revenue_leak_detector | sf_revenue_leakage_analyzer | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_battle_rhythm | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_asset_library | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_battlecard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battle_rhythm | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_capacity_model | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_battlecard | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_commission_simulation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_capacity_model | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_commission_statement | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_enablement_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_forecast_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_onboarding_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_play_execution | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_dashboard | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_coaching_effectiveness | sf_sales_coaching_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_plan | sf_supplier_risk_dashboard | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_plan | sf_telework_policy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_plan | sf_upsell_trigger_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_content_library | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_simulation | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_enablement_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_forecast_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_onboarding_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_play_execution | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_commission_statement | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_sales_forecast_category | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_content_library | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_forecast_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_onboarding_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_play_execution | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_enablement_tracker | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_sales_onboarding_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_sales_play_execution | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_accuracy | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_sales_gamification | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_forecast_category | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_sales_hiring_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_gamification | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_sales_hiring_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_plan | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_sales_huddle_notes | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_hiring_tracker | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_service_level_agreement_monitor | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_huddle_notes | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_onboarding_plan | sf_sales_play_execution | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_onboarding_plan | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_onboarding_plan | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_onboarding_plan | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_onboarding_plan | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_play_execution | sf_sales_target_cascade | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_play_execution | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_play_execution | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_play_execution | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_target_cascade | sf_sales_territory_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_target_cascade | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_target_cascade | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_territory_planner | sf_sales_territory_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_territory_planner | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_sales_territory_review | sf_territory_mapping | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_supplier_invoice_3way_match3 | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_service_level_agreement_monitor | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_program | sf_supplier_pareto_abc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_program | sf_supplier_performance_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_capacity_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_capacity_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_audit_scheduler | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_forecast | sf_supplier_leadtime_audit | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_forecast | sf_supplier_pricing_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_forecast | sf_supplier_pricing_history | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_forecast | sf_supplier_pricing_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_forecast | sf_supplier_pricing_tiers | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_capacity_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_planner | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_contract_database | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_capacity_review | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_contract_renewal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_database | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_contract_renewal_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_diversity_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_contract_renewal_tracker | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_invoice_3way_match | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_diversity_tracker | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_invoice_accuracy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_supplier_invoice_matching | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_3way_match3 | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_onboarding_checklist | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_accuracy | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_system_health_check | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_invoice_matching | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_leadtime_audit | sf_supplier_pricing_benchmark | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_leadtime_audit | sf_supplier_pricing_history | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_leadtime_audit | sf_supplier_pricing_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_leadtime_audit | sf_supplier_pricing_tiers | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_onboarding_portal | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_checklist | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_supplier_payment_optimization | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_onboarding_portal | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pareto_abc | sf_supplier_performance_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_supplier_payment_terms | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_optimization | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_terms | sf_supplier_risk_mitigation | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_terms | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_terms | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_terms | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_payment_terms | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_benchmark | sf_supplier_pricing_history | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_benchmark | sf_supplier_pricing_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_benchmark | sf_supplier_pricing_tiers | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_history | sf_supplier_pricing_review | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_history | sf_supplier_pricing_tiers | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_pricing_review | sf_supplier_pricing_tiers | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_dashboard | sf_telework_policy | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_dashboard | sf_upsell_trigger_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation | sf_supplier_risk_mitigation_plan | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation_plan | sf_supplier_risk_score | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation_plan | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_mitigation_plan | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_score | sf_third_party_risk | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_supplier_risk_score | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_tax_provision_calc | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_system_health_check | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_tax_provision_calc | sf_training_budget | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_tax_provision_calc | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_tax_provision_calc | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_tax_provision_calc | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_tax_provision_calc | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_telework_policy | sf_upsell_trigger_rules | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_third_party_risk | sf_vendor_scorecard_auto | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_training_budget | sf_warehouse_layout_planner | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_training_budget | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_training_budget | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_training_budget | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_layout_planner | sf_warehouse_safety_log | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_layout_planner | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_layout_planner | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_safety_log | sf_warehouse_throughput | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_safety_log | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |
| sf_warehouse_throughput | sf_waste_stream_tracker | 52.0% | 0% | 60.0% | 100.0% | 100.0% | Potential duplicate (review needed) |

## Security Issues - eval()/exec() Usage

No eval/exec issues found.

## sudo() Usage Analysis

| Module | File | Line | Context |
|--------|------|------|---------|
| sf_aql_sampling | sf_aql_sampling\models\sf_aql_inspection.py | 90 | self.env['ir.config_parameter'].sudo() |
| sf_aql_sampling | sf_aql_sampling\models\sf_aql_inspection.py | 108 | self.env['ir.config_parameter'].sudo() |
| sf_aql_sampling | sf_aql_sampling\tests\test_sf_aql_sampling.py | 206 | self.env['ir.config_parameter'].sudo() |
| sf_batch_records | sf_batch_records\models\sf_batch_record.py | 101 | self.env['ir.config_parameter'].sudo() |
| sf_business_travel | sf_business_travel\models\sf_business_travel.py | 159 | self.env['ir.config_parameter'].with_company(company).sudo() |
| sf_cold_chain | sf_cold_chain\models\sf_cold_excursion.py | 114 | self.env['ir.config_parameter'].sudo() |
| sf_cold_chain | sf_cold_chain\tests\test_sf_cold_chain.py | 219 | self.env['ir.config_parameter'].sudo() |
| sf_courier_delivery | sf_courier_delivery\models\sf_courier_delivery.py | 55 | self.env['ir.config_parameter'].sudo() |
| sf_courier_delivery | sf_courier_delivery\models\sf_courier_order.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_delivery.py | 152 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_key.py | 76 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 31 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 34 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 43 | self.env['ir.config_parameter'].sudo() |
| sf_direct_print_pro | sf_direct_print_pro\models\print_printer.py | 116 | self.report_id.sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 81 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 132 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 187 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 62 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 70 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 107 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 165 | self.env['ir.config_parameter'].sudo() |
| sf_equipment_rental | sf_equipment_rental\models\sf_rental_contract.py | 154 | self.env['ir.config_parameter'].sudo() |
| sf_events | sf_events\models\sf_event.py | 95 | scoped.env['ir.config_parameter'].sudo() |
| sf_events | sf_events\tests\test_sf_events.py | 162 | event.sudo() |
| sf_franchise | sf_franchise\models\sf_franchise_declaration.py | 73 | self.env['ir.config_parameter'].sudo() |
| sf_franchise | sf_franchise\models\sf_franchise_declaration.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_freight_audit | sf_freight_audit\models\sf_freight_dispute.py | 101 | d.invoice_id.sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\models\sf_gift_hospitality.py | 60 | self.env['ir.config_parameter'].sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\tests\test_sf_gifts_hospitality.py | 45 | self.env['ir.config_parameter'].sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\tests\test_sf_gifts_hospitality.py | 54 | self.env['ir.config_parameter'].sudo() |
| sf_ic_netting | sf_ic_netting\models\ic_models.py | 172 | self.env['ir.config_parameter'].sudo() |
| sf_invoice_matching | sf_invoice_matching\models\account_move.py | 52 | move.sudo() |
| sf_invoice_matching | sf_invoice_matching\models\account_move.py | 212 | move.sudo() |
| sf_laundry | sf_laundry\models\sf_laundry_order.py | 124 | scoped.env['ir.config_parameter'].sudo() |
| sf_laundry | sf_laundry\models\sf_laundry_order.py | 46 | self.env['ir.config_parameter'].sudo() |
| sf_lease_ifrs16 | sf_lease_ifrs16\models\lease_contract.py | 370 | self.env['ir.config_parameter'].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 22 | request.env[model].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 45 | request.env[model].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 61 | request.env['mcp.server'].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 76 | request.env['mcp.request.log'].sudo() |
| sf_parking_management | sf_parking_management\models\sf_parking_site.py | 39 | self.env['ir.config_parameter'].sudo() |
| sf_parking_management | sf_parking_management\models\sf_parking_subscription.py | 66 | self.env['ir.config_parameter'].sudo() |
| sf_period_close | sf_period_close\models\close_models.py | 158 | rec.period_id.sudo() |
| sf_pharmacy | sf_pharmacy\models\res_config_settings.py | 13 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\models\res_config_settings.py | 22 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\models\sf_pharmacy_batch.py | 178 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\tests\test_sf_pharmacy.py | 183 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\tests\test_sf_pharmacy.py | 198 | self.env['ir.config_parameter'].sudo() |
| sf_policy_acknowledgment | sf_policy_acknowledgment\models\sf_policy.py | 144 | self.env['ir.config_parameter'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 47 | self.env['sale.order.line'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 71 | self.env['ir.config_parameter'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 73 | self.env['ir.config_parameter'].sudo() |
| sf_restaurant | sf_restaurant\models\sf_restaurant_reservation.py | 117 | scoped.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\models\sf_rework_order.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\models\sf_rework_order.py | 151 | self.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\tests\test_sf_rework_management.py | 162 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\models\sf_salon_service.py | 33 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\models\sf_salon_staff.py | 23 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\tests\test_sf_salon_beauty.py | 185 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\tests\test_sf_salon_beauty.py | 186 | self.env['ir.config_parameter'].sudo() |
| sf_senior_living | sf_senior_living\wizard\billing_wizard.py | 249 | self.env['ir.config_parameter'].sudo() |
| sf_senior_living | sf_senior_living\wizard\billing_wizard.py | 277 | self.env['ir.config_parameter'].sudo() |
| sf_staffing | sf_staffing\models\sf_staffing_mission.py | 189 | self.env['ir.config_parameter'].sudo() |
| sf_store_credit | sf_store_credit\models\sf_store_credit.py | 180 | self.env['ir.config_parameter'].sudo() |
| sf_trade_promotions | sf_trade_promotions\models\sf_trade_claim.py | 71 | self.env['ir.config_parameter'].sudo() |
| sf_trade_promotions | sf_trade_promotions\models\sf_trade_program.py | 74 | expired.sudo() |
| sf_travel_agency | sf_travel_agency\models\res_config_settings.py | 23 | self.env['ir.config_parameter'].sudo() |
| sf_travel_agency | sf_travel_agency\models\sf_travel_package.py | 80 | self.env['ir.config_parameter'].sudo() |
| sf_travel_agency | sf_travel_agency\models\sf_travel_reservation.py | 41 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\models\sf_utility_invoice.py | 68 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\models\sf_utility_meter.py | 58 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\tests\test_sf_utility_billing.py | 141 | self.env['ir.config_parameter'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 13 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 23 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 33 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 43 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 53 | request.env['purchase.order'].sudo() |

## Empty Methods (Stubs)

No empty methods found.

## Modules Missing Tests

sf_access_request_workflow, sf_access_review, sf_accrual_proposals, sf_accrual_reversal_auto, sf_anniversary_reminders, sf_api_integration_log, sf_asset_count_campaign, sf_asset_disposal_request, sf_backorder_priority, sf_backup_verification_log, sf_bank_fee_analytics, sf_bank_reconciliation_rules, sf_bank_stmt_import_pro, sf_batch_job_monitor, sf_blanket_order_release, sf_bom_change_request, sf_budget_virement, sf_budget_vs_actual_alerts, sf_business_glossary, sf_business_requirement, sf_capacity_forecast_sales, sf_capacity_planner, sf_capex_requests, sf_capital_expenditure_plan, sf_carrier_performance, sf_certificate_requests, sf_change_freeze_calendar, sf_change_requests, sf_checklist_library, sf_churn_prediction_rules, sf_commission_clawback, sf_committee_decisions, sf_company_car_policy, sf_compensation_benchmark, sf_competitive_intel_register, sf_compliance_calendar, sf_compliance_obligation, sf_contract_compliance_audit, sf_credit_insurance, sf_credit_note_reasons, sf_cross_sell_engine, sf_crossdock_operations, sf_currency_exposure_map, sf_customer_advisory_board, sf_customer_advocacy_program, sf_customer_care_coaching, sf_customer_care_coaching_plan, sf_customer_care_escalation, sf_customer_care_escalation_dashboard, sf_customer_care_escalation_matrix, sf_customer_care_escalation_rules, sf_customer_care_escalation_tracker, sf_customer_care_journey, sf_customer_care_program, sf_customer_care_qa_review, sf_customer_care_qa_scorecard, sf_customer_care_satisfaction, sf_customer_care_satisfaction_survey, sf_customer_care_sla, sf_customer_care_sla_breach, sf_customer_care_sla_dashboard, sf_customer_care_sla_rules, sf_customer_care_survey, sf_customer_care_training, sf_customer_care_training_plan, sf_customer_care_workforce, sf_customer_care_workforce_plan, sf_customer_care_workload, sf_customer_churn_analytics, sf_customer_complaint_praise, sf_customer_contract_renewal_forecast, sf_customer_contract_renewal_pipeline, sf_customer_covenant_tracker, sf_customer_document_vault, sf_customer_escalation_matrix, sf_customer_expansion_tracker, sf_customer_feedback_actions, sf_customer_feedback_analytics, sf_customer_health, sf_customer_health_scoring, sf_customer_incident_comms, sf_customer_journey_analytics, sf_customer_journey_map, sf_customer_journey_mapper, sf_customer_journey_stage, sf_customer_onboarding, sf_customer_onboarding_checklist, sf_customer_onboarding_cost, sf_customer_onboarding_docs, sf_customer_pain_point, sf_customer_payment_behavior, sf_customer_payment_plan, sf_customer_portal_tasks, sf_customer_pricing_requests, sf_customer_priority_matrix, sf_customer_profitability_rank, sf_customer_rebates, sf_customer_reference_program, sf_customer_reference_tracker, sf_customer_revenue_trend, sf_customer_risk_score, sf_customer_satisfaction_trend, sf_customer_segment_rules, sf_customer_segments_rules, sf_customer_visit_reports, sf_cycle_count_scheduler, sf_damaged_goods_log, sf_data_dedup, sf_data_quality_check, sf_deal_desk_request, sf_decision_log, sf_demand_planning_review, sf_disciplinary_action, sf_dividend_register, sf_document_approval_hybrid, sf_dr_plan_tracker, sf_dropship_operations, sf_ehs_inspection_schedule, sf_emergency_purchase_log, sf_employee_1on1_tracker, sf_employee_asset_return, sf_employee_engagement_action, sf_employee_referral, sf_employee_skill_gap, sf_employee_survey, sf_energy_meter_readings, sf_energy_saving_tracker, sf_environmental_waste_tracking, sf_equipment_utilization, sf_exit_interviews, sf_expiry_alert_manager, sf_external_audit_tracker, sf_facility_management, sf_field_service_checklist, sf_field_service_customer_satisfaction, sf_field_service_dispatch, sf_field_service_parts, sf_financial_covenant_monitor, sf_financial_ratio_dashboard, sf_first_piece_validation, sf_fixed_asset_transfer, sf_freight_quote_compare, sf_fx_hedge_accounting, sf_fx_hedging, sf_fx_reval_scheduler, sf_grievance_tracker, sf_iatf_quality_suite, sf_ic_netting, sf_incident_oncall, sf_incident_postmortem, sf_intercompany_balance_check, sf_intercompany_loan, sf_interim_billing_tracker, sf_internal_audit_program, sf_internal_mobility, sf_internship_tracker, sf_inventory_abc_classification, sf_inventory_accuracy_rate, sf_inventory_aging, sf_inventory_count_variance, sf_inventory_revaluation, sf_inventory_shrinkage_tracker, sf_inventory_turnover_analysis, sf_inventory_writeoff_register, sf_invoice_discounting, sf_it_asset_lifecycle, sf_it_capacity_planning, sf_job_costing_snapshot, sf_key_account_plans, sf_knowledge_articles, sf_kpi_target_register, sf_kyc_aml, sf_late_payment_interest, sf_lease_ifrs16, sf_line_balancing_review, sf_load_planning, sf_maintenance_cost_tracker, sf_maintenance_intake, sf_maintenance_schedule_optimizer, sf_management_reporting, sf_marketing_budget_tracker, sf_marketing_campaign_roi, sf_meeting_minutes, sf_mgmt_fee_billing, sf_min_order_enforcement, sf_minmax_review, sf_multi_site_price_harmony, sf_nonconformance_cost, sf_obsolescence_forecast, sf_onboarding_cost, sf_oncall_schedule, sf_ooo_calendar, sf_operator_skill_matrix, sf_order_freeze_windows, sf_overtime_preapproval, sf_packaging_spec_register, sf_pallet_sscc_labels, sf_payment_milestone_engine, sf_payroll_deadline_tracker, sf_peak_season_planning, sf_period_close, sf_po_acknowledgment, sf_po_amendment_log, sf_po_budget_check, sf_policy_exception_tracker, sf_policy_waivers, sf_prepaid_amortization, sf_price_change_mgmt, sf_probation_review_tracker, sf_procurement_savings_tracker, sf_product_eol, sf_product_lifecycle_stage, sf_product_margin_matrix, sf_product_return_rate, sf_product_return_reasons, sf_production_capacity_plan, sf_production_capacity_review, sf_production_capacity_whatif, sf_production_downtime_pareto, sf_production_line_efficiency, sf_production_meeting_actions, sf_production_oee_calculator, sf_production_oee_dashboard, sf_production_oee_tracker, sf_production_order_priority, sf_production_order_sequencing, sf_production_scenarios, sf_production_schedule_alert, sf_production_scrap_analytics, sf_production_scrap_pareto, sf_production_trial_tracking, sf_production_waste_tracker, sf_production_yield_analysis, sf_production_yield_tracker, sf_project_change_request, sf_project_charter, sf_project_lessons_learned, sf_project_milestone_tracker, sf_project_portfolio_board, sf_project_resource_plan, sf_project_risk_log, sf_project_stakeholder, sf_provision_register, sf_purchase_approval_matrix, sf_purchase_contract_compliance, sf_purchase_envelope, sf_purchase_order_aging, sf_purchase_price_analysis, sf_purchase_requisition_analytics, sf_purchase_requisition_template, sf_quality_alert_aging, sf_quality_alert_auto_assign, sf_quality_alert_escalation, sf_quality_audit_program, sf_quality_coa, sf_quality_cost_tracker, sf_quality_document_control, sf_quality_document_control_sys, sf_quality_hold_register, sf_quality_inspection_mobile2, sf_quality_inspection_plan, sf_quality_inspection_planner, sf_quality_pareto_analyzer, sf_quality_pareto_update, sf_quality_trend_dashboard, sf_quote_followup_cadence, sf_receiving_discrepancy_log, sf_recurring_cost_register, sf_recurring_revenue_register, sf_recurring_task_templates, sf_regulatory_watch, sf_remote_work_requests, sf_renewal_management, sf_replenishment_review, sf_retention_schedule, sf_return_to_vendor, sf_revenue_backlog_tracker, sf_revenue_leak_detector, sf_revenue_leakage_analyzer, sf_revenue_milestone, sf_revenue_protection_plan, sf_runbook_library, sf_safety_inspections, sf_safety_training_tracker, sf_sales_asset_library, sf_sales_battle_rhythm, sf_sales_battlecard, sf_sales_capacity_model, sf_sales_coaching_dashboard, sf_sales_coaching_effectiveness, sf_sales_coaching_log, sf_sales_coaching_plan, sf_sales_commission_plan, sf_sales_commission_simulation, sf_sales_commission_statement, sf_sales_content_library, sf_sales_enablement_tracker, sf_sales_forecast_accuracy, sf_sales_forecast_category, sf_sales_gamification, sf_sales_hiring_funnel, sf_sales_hiring_plan, sf_sales_hiring_tracker, sf_sales_huddle_notes, sf_sales_hygiene_audit, sf_sales_onboarding_plan, sf_sales_order_acknowledgment, sf_sales_pipeline_review, sf_sales_play_execution, sf_sales_playbook, sf_sales_target_cascade, sf_sales_territory_planner, sf_sales_territory_review, sf_sample_management, sf_scrap_reason_analytics, sf_sell_through_reporting, sf_service_catalog, sf_service_level_agreement_monitor, sf_shift_swap_board, sf_sla_pause_tracking, sf_software_license_renewals, sf_spare_parts_minmax, sf_special_price_approval, sf_spend_analytics, sf_stock_adjustment_approval, sf_succession_plan, sf_supplier_audit_program, sf_supplier_audit_scheduler, sf_supplier_bank_change_alert, sf_supplier_capacity_check, sf_supplier_capacity_forecast, sf_supplier_capacity_planner, sf_supplier_capacity_review, sf_supplier_contract_database, sf_supplier_contract_renewal, sf_supplier_contract_renewal_alert, sf_supplier_contract_renewal_tracker, sf_supplier_diversity_tracker, sf_supplier_invoice_3way_match, sf_supplier_invoice_3way_match3, sf_supplier_invoice_accuracy, sf_supplier_invoice_matching, sf_supplier_leadtime_audit, sf_supplier_negotiation_prep, sf_supplier_onboarding_checklist, sf_supplier_onboarding_portal, sf_supplier_pareto_abc, sf_supplier_payment_optimization, sf_supplier_payment_terms, sf_supplier_performance_dashboard, sf_supplier_performance_review, sf_supplier_pricing_benchmark, sf_supplier_pricing_history, sf_supplier_pricing_review, sf_supplier_pricing_tiers, sf_supplier_questionnaire, sf_supplier_rebates, sf_supplier_risk_dashboard, sf_supplier_risk_mitigation, sf_supplier_risk_mitigation_plan, sf_supplier_risk_register, sf_supplier_risk_score, sf_supplier_scorecard_review, sf_system_health_check, sf_tax_deadline_calendar, sf_tax_provision_calc, sf_telecom_expense, sf_telework_policy, sf_territory_mapping, sf_third_party_risk, sf_tooling_request, sf_training_budget, sf_training_feedback, sf_transfer_pricing, sf_treasury_week_board, sf_upsell_trigger_rules, sf_user_activity_log, sf_vendor_sample_tracking, sf_vendor_scorecard_auto, sf_vendor_sla_monitor, sf_warehouse_layout_planner, sf_warehouse_safety_log, sf_warehouse_slotting_review, sf_warehouse_throughput, sf_warehouse_throughput_daily, sf_warning_letter_register, sf_warranty_cost_analytics, sf_waste_stream_tracker, sf_win_loss_analysis, sf_workorder_handover, sf_yard_management, sf_zone_capacity_monitor

## AI Modules - Implementation Gap Analysis

| Module | Claims | Has External Deps | Has API Key Config |
|--------|--------|-------------------|---------------------|
| sf_ai_contract_analyzer | Extract obligations, dates, risks from contracts (PDF/Word) with AI - auto calendar alerts AI Contra... | False | False |
| sf_ai_demand_forecast | ML-powered demand forecasting for inventory optimization AI Demand Forecasting
=====================... | False | False |
| sf_ai_doc_intelligence | Classify, extract & route documents (invoices, contracts, CVs, claims) with AI AI Document Intellige... | False | False |
| sf_asset_count_campaign | Physical asset count campaigns: scan/verify assets vs ledger with discrepancy log. 
Fixed Asset Phys... | False | False |
| sf_automation_builder | Zapier-like visual builder: triggers → actions → conditions for Odoo models + external APIs Visual N... | False | False |
| sf_cold_chain | Monitor temperature excursions on cold storage sites and transport trips with alerts and reports ... | False | False |
| sf_complaint_8d | 8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notificat... | False | False |
| sf_customer_care_training | Track customer care team training: modules, scores and certification status. 
Customer Care Training... | False | False |
| sf_customer_care_training_plan | Training plans for care team: modules, scores, certifications and refreshers. 
Care Training Plan
==... | False | False |
| sf_customer_complaint_praise | Capture customer compliments and praise: team recognition, root strengths and sharing. 
Customer Com... | False | False |
| sf_customer_pain_point | Register customer pain points: description, severity, product impact and resolution status. 
Custome... | False | False |
| sf_first_article_inspection | First Article Inspection per AS9102/AS9145 for aerospace/automotive 
First Article Inspection (FAI)
... | False | False |
| sf_iatf_quality_suite | Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, M... | False | False |
| sf_lead_scoring_ai | Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams. ... | False | False |
| sf_maintenance_cost_tracker | Track maintenance costs per equipment: preventive, corrective, parts and labor. 
Maintenance Cost Tr... | False | False |
| sf_maintenance_intake | Internal maintenance request intake: priority triage, assignment and resolution feedback. 
Maintenan... | False | False |
| sf_maintenance_schedule_optimizer | Optimize maintenance schedules: equipment criticality, usage and production impact. 
Maintenance Sch... | False | False |
| sf_marketing_campaign_roi | Track marketing campaigns: spend, leads, conversions and ROI computation. 
Marketing Campaign ROI Tr... | False | False |
| sf_mcp_server_pro | Connect AI assistants to your Odoo instance securely ... | False | False |
| sf_prepaid_amortization | Track prepaid expenses (insurance, subscriptions, rent) with monthly amortization schedules. 
Prepai... | False | False |
| sf_preventive_maintenance_pro | PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.... | False | False |
| sf_privacy_rgpd | Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights manage... | False | False |
| sf_safety_training_tracker | Track mandatory safety training per employee with expiry and compliance rate. 
Safety Training Compl... | False | False |
| sf_supplier_questionnaire | Send compliance/ESG questionnaires to suppliers with response tracking and scoring. 
Supplier Questi... | False | False |
| sf_training_budget | Training budget per department: allocated, spent, remaining and ROI. 
Training Budget Tracker
======... | False | False |
| sf_training_certifications | Track employee trainings, sessions, registrations and certifications with expiry alerts 
Training & ... | False | False |
| sf_training_feedback | Collect structured feedback per training session: ratings, comments and improvement actions. 
Traini... | False | False |
| sf_warehouse_throughput_daily | Daily warehouse throughput: orders, lines, picks per hour and error rates. 
Daily Warehouse Throughp... | False | False |
| sf_warranty_claims_portal | Customer self-service warranty claims with SLA tracking and automatic credit note. ... | False | False |

## Manifest Issues

No manifest parsing issues.

## Versioned __pycache__ Files

No __pycache__ files found.

## Module-by-Module Details

### sf_access_request_workflow

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request system access: role, system, justification, approver and provisioning.

### sf_access_review

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions and evidence

### sf_access_rights_manager

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Granular permissions without developer mode

### sf_accrual_proposals

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Propose, approve and reverse month-end accruals with automatic reversal tracking.

### sf_accrual_reversal_auto

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Auto-reverse prior month accruals with tracking and exception report.

### sf_agriculture

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Farms, plots, campaigns, cultures, treatments, harvests and inputs register for agriculture

### sf_ai_contract_analyzer

- **Models:** None
- **Depends:** base, mail, account, hr, fleet
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Extract obligations, dates, risks from contracts (PDF/Word) with AI - auto calendar alerts

### sf_ai_demand_forecast

- **Models:** None
- **Depends:** base, stock, sale
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** ML-powered demand forecasting for inventory optimization

### sf_ai_doc_intelligence

- **Models:** None
- **Depends:** base, mail, account, hr, helpdesk
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Classify, extract & route documents (invoices, contracts, CVs, claims) with AI

### sf_ai_invoice_ocr

- **Models:** None
- **Depends:** base, account, hr_expense
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Scan invoices & expenses with AI OCR (Mistral, Gemini, Claude)

### sf_anniversary_reminders

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Work anniversaries and birthdays with upcoming lists and celebration tracking.

### sf_api_integration_log

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log API integrations: endpoint, direction, status, latency and error tracking.

### sf_approval_engine

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Reusable multi-step approval workflows for any document (PO, expenses, leave, etc.)

### sf_aql_sampling

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Statistical acceptance sampling: AQL inspection plans, lot inspections, defect recording and accept/reject decisions

### sf_asset_count_campaign

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Physical asset count campaigns: scan/verify assets vs ledger with discrepancy log.

### sf_asset_depreciation_pro

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Multi-method depreciation (straight-line, declining, units) with component accounting and revaluation.

### sf_asset_disposal_request

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request asset disposal: reason, valuation method, approval and execution.

### sf_automation_builder

- **Models:** None
- **Depends:** base, mail, web
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Zapier-like visual builder: triggers → actions → conditions for Odoo models + external APIs

### sf_backorder_priority

- **Models:** None
- **Depends:** base, sale, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Allocate scarce stock to open backorders by configurable priority rules (customer segment, value, promised date)

### sf_backup_verification_log

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log backup jobs with verification results, restore tests and failure follow-ups.

### sf_bank_fee_analytics

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze bank charges per account/month: categories, trends and savings opportunities.

### sf_bank_loans

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track bank loans, calculated amortization schedules, drawdowns, early repayments and covenants with alerts

### sf_bank_reconciliation_rules

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Build reusable bank statement reconciliation rules with priority, match percentages and auto-suggest application.

### sf_bank_stmt_import_pro

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 6
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Import any bank statement: MT940, CAMT.053, OFX, QIF or any bank CSV - per-bank templates, duplicate detection, multi-currency

### sf_barcode_label_designer

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Drag-and-drop label designer with barcode/QR support, ZPL and PDF output, batch printing.

### sf_batch_job_monitor

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor scheduled batch jobs: cron name, last run, duration, status and failures.

### sf_batch_records

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Electronic batch production records: materials, steps, parameters, deviations, QA review and lot release

### sf_blanket_order_release

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage blanket POs: total quantity, released quantities, remaining balance and expiry alerts.

### sf_bom_change_request

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request and approve BOM changes: component swaps, qty changes with effectivity dates and cost impact.

### sf_budget_virement

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request and approve budget transfers between analytic accounts or departments with audit trail.

### sf_budget_vs_actual_alerts

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monthly budget consumption per department with threshold alerts (80%, 100%).

### sf_business_continuity

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Resilience ISO 22301: critical processes BIA, continuity strategies, recovery plans, exercises and review alerts

### sf_business_glossary

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shared business terms: definition, owner, source system and related KPIs.

### sf_business_requirement

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register business requirements: source, priority, complexity and implementation status.

### sf_business_travel

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Employee travel requests, approval workflow, itinerary lines, budget tracking and mission orders

### sf_capacity_forecast_sales

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sales team capacity: reps, working days, expected pipeline coverage vs targets.

### sf_capacity_planner

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan team capacity: members, availability, allocation and over-allocation alerts.

### sf_capex_requests

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capital expenditure requests with multi-level approvals, ROI/payback fields, budget check and capitalization tracking

### sf_capital_expenditure_plan

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Multi-year capital expenditure planning with depreciation forecasting.

### sf_carrier_performance

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track carrier on-time delivery, damage rate and claims per month with scorecards.

### sf_cash_flow_forecast

- **Models:** None
- **Depends:** base, account, purchase
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Forecast cash position, track receivables/payables and avoid liquidity gaps

### sf_certificate_requests

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Work certificate, salary attestation and employment letter requests with template generation.

### sf_change_freeze_calendar

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Change freeze windows (fiscal close, peak season) blocking non-emergency changes.

### sf_change_requests

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** IT and operational changes with CAB review, risk levels, rollback plans and post-implementation closure

### sf_checklist_library

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Build reusable checklists (audits, onboarding, launches) and run instances with progress.

### sf_churn_prediction_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define churn prediction rules: usage signals, weights, thresholds and alert actions.

### sf_cleaning

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Cleaning service contracts, schedules, interventions, quality checks and invoicing

### sf_cold_chain

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Monitor temperature excursions on cold storage sites and transport trips with alerts and reports

### sf_commission_clawback

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Claw back commissions on returned or unpaid orders: rules, cases and recovery tracking.

### sf_committee_decisions

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log committee/steering decisions: context, options, decision, voters and follow-up actions.

### sf_community_center

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Community center management: spaces, activities, memberships, ticketing, grants

### sf_company_car_policy

- **Models:** None
- **Depends:** base, hr, fleet, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Company car assignments: eligibility per grade, CO2 bands, fuel card and contract end.

### sf_compensation_benchmark

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Salary benchmarking per role/grade with market data and compa-ratio.

### sf_competitive_intel_register

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register competitive intel: competitor moves, product updates, pricing changes.

### sf_complaint_8d

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** 8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notification.

### sf_compliance_calendar

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** All compliance deadlines (tax, audit, safety, env) with owners and status.

### sf_compliance_obligation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register all compliance obligations: regulation, requirement, evidence and deadline.

### sf_compliance_register

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track licenses, permits, certifications and insurance expirations with alerts

### sf_consolidation

- **Models:** None
- **Depends:** base, account
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Consolidate P&L data across companies and currencies

### sf_construction_boq

- **Models:** None
- **Depends:** base, project, product, account, uom
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Bill of Quantities, subcontract management and progress billing (IPC) for construction

### sf_contract_compliance_audit

- **Models:** None
- **Depends:** base, purchase, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Audit invoices against supplier contracts: price compliance, SLA adherence and breach log.

### sf_corporate_capital

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shareholders, share classes, capital movements (issue/transfer/buyback), issued shares, cap table and share certificates

### sf_corporate_secretary

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Corporate secretariat: organs, AG/board meetings, convocations, resolutions, votes, minutes, written decisions and regulatory deadlines

### sf_correspondence

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Incoming and outgoing correspondence register with routing, response deadlines and registered mail tracking

### sf_courier_delivery

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Pickup/delivery requests, courier assignment, routes, delivery proof (photo/signature), failures, returns and invoicing

### sf_cpq_configurator

- **Models:** None
- **Depends:** base, sale, product, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure custom products, compute prices and generate quotes

### sf_creche

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Children, enrollments, daily attendance, room capacity control and monthly hourly billing

### sf_credit_insurance

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Insurer policies, approved buyer limits with coverage %, and bad-debt claims with indemnity tracking

### sf_credit_note_reasons

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mandatory reason codes on credit notes with monthly analytics and corrective actions.

### sf_cross_sell_engine

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define product affinity rules for cross-sell recommendations at quote time.

### sf_crossdock_operations

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log cross-dock flows: inbound arrival, outbound link, dwell time and priority handling.

### sf_currency_exposure_map

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Net open FX position per currency pair with hedging recommendation.

### sf_custom_report_builder

- **Models:** None
- **Depends:** base, sale, account, stock, purchase
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Design professional PDF reports without code

### sf_customer_advisory_board

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage advisory board members: meetings, topics discussed and feedback collected.

### sf_customer_advocacy_program

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Identify and manage customer advocates: reference calls, case studies, testimonials.

### sf_customer_care_coaching

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log coaching sessions for care team: quality review, feedback and improvement areas.

### sf_customer_care_coaching_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured coaching plans for care agents: skills, development areas and milestones.

### sf_customer_care_escalation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer escalations: tier, reason, resolution time and satisfaction after resolution.

### sf_customer_care_escalation_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure escalation dashboards: metrics, thresholds, alert rules and team routing.

### sf_customer_care_escalation_matrix

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define customer care escalation matrix: tiers, triggers, contacts and response times.

### sf_customer_care_escalation_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define escalation rules: triggers, tiers, timers and notification chains.

### sf_customer_care_escalation_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer escalations: tier, reason, resolution and satisfaction.

### sf_customer_care_journey

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Map customer care journey: touchpoints, satisfaction per touchpoint and improvement areas.

### sf_customer_care_program

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Scheduled care touches per key customer: cadence, last contact, next action and satisfaction.

### sf_customer_care_qa_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Quality assurance review of customer interactions: scoring grid, feedback and coaching.

### sf_customer_care_qa_scorecard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** QA scorecards for customer care: interaction review, scoring and coaching links.

### sf_customer_care_satisfaction

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capture satisfaction after each customer interaction: rating, comments and follow-up.

### sf_customer_care_satisfaction_survey

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Send post-resolution surveys: CSAT, effort score and open text feedback.

### sf_customer_care_sla

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer care SLAs: first response, resolution time and escalation per tier.

### sf_customer_care_sla_breach

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze SLA breaches: root causes, trends and prevention actions per team.

### sf_customer_care_sla_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure care SLA dashboards: metrics, targets and alert rules per tier.

### sf_customer_care_sla_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define care SLA rules: tier, metric, target, escalation and breach actions.

### sf_customer_care_survey

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Run customer care surveys: NPS, CSAT, CES with response tracking and actions.

### sf_customer_care_training

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer care team training: modules, scores and certification status.

### sf_customer_care_training_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Training plans for care team: modules, scores, certifications and refreshers.

### sf_customer_care_workforce

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan customer care workforce: forecast volume, staff needed, shift coverage and skills.

### sf_customer_care_workforce_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan customer care workforce: volume forecast, staff needed, shift coverage and skills.

### sf_customer_care_workload

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Balance care workload: open cases per agent, capacity and redistribution suggestions.

### sf_customer_churn_analytics

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze churned customers: reasons, revenue lost, win-back opportunities.

### sf_customer_complaint_praise

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capture customer compliments and praise: team recognition, root strengths and sharing.

### sf_customer_contract_renewal_forecast

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Forecast renewal revenue by month based on contract expiry dates and historical win rates.

### sf_customer_contract_renewal_pipeline

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pipeline of contract renewals: expiry timeline, renewal probability and revenue forecast.

### sf_customer_covenant_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track contract covenants (minimum purchases, exclusivity) with compliance status.

### sf_customer_credit_limits

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated credit limit enforcement with blocking, escalation workflow and exposure dashboard.

### sf_customer_document_vault

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Customer document requirements: signed contracts, insurance certs, audits with expiry alerts.

### sf_customer_escalation_matrix

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define escalation paths per customer tier: contacts, response times and authority levels.

### sf_customer_expansion_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track expansion opportunities: upsell, cross-sell, new department and land-and-expand.

### sf_customer_feedback_actions

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Convert customer feedback into tracked actions with owners, due dates and closure validation.

### sf_customer_feedback_analytics

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze customer feedback: themes, sentiment, trends and action prioritization.

### sf_customer_health

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Post-sale health scoring per customer: revenue recency, trend and overdue signals with churn risk rating

### sf_customer_health_scoring

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define health scoring rules: signals, weights, thresholds and alert triggers.

### sf_customer_incident_comms

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage customer communications during incidents: who to inform, messages sent, feedback.

### sf_customer_journey_analytics

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze customer journey stages: time in stage, conversion rates and drop-off points.

### sf_customer_journey_map

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customers through journey stages: awareness to advocacy with touchpoints.

### sf_customer_journey_mapper

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Map customer journey stages: touchpoints, experience scores and drop-off analysis.

### sf_customer_journey_stage

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer journey stages: awareness, consideration, decision with touchpoint counts.

### sf_customer_onboarding

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured customer onboarding: document checklist, setup tasks, progress tracking and first-order follow-up

### sf_customer_onboarding_checklist

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured customer onboarding checklists: documents, setup, training and go-live.

### sf_customer_onboarding_cost

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track cost to onboard each customer: hours, resources and total cost per customer.

### sf_customer_onboarding_docs

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request and track document collection from customers (specs, drawings, compliance forms).

### sf_customer_pain_point

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register customer pain points: description, severity, product impact and resolution status.

### sf_customer_payment_behavior

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze payment patterns: avg days-to-pay, trend, risk score per customer.

### sf_customer_payment_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Set up payment plans for customers: installments, due dates and tracking.

### sf_customer_portal_pro

- **Models:** None
- **Depends:** base, website, sale, account, portal, payment
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** B2B/B2C portal: invoices, payments, subscriptions, returns, tickets, documents

### sf_customer_portal_tasks

- **Models:** None
- **Depends:** base, sale, portal, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Task exchange with customers via portal: request, deliverable, validation loop.

### sf_customer_pricing_requests

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log customer pricing requests (RFQs): response time, win rate and pricing pressure analytics.

### sf_customer_priority_matrix

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Classify customers A/B/C by revenue and strategic value driving service level decisions.

### sf_customer_profitability_rank

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Rank customers by profitability: revenue, direct costs, service costs, net margin.

### sf_customer_rebates

- **Models:** None
- **Depends:** base, account, sale, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sell-side rebate deals (retro %, turnover bonus, per unit) with accrual from invoices and credit note settlement

### sf_customer_reference_program

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage customer references: use cases, availability and sales team usage.

### sf_customer_reference_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track reference customers: use cases, contacts willing to talk, and usage in sales.

### sf_customer_revenue_trend

- **Models:** None
- **Depends:** base, account, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect customers with revenue drops beyond thresholds for proactive action.

### sf_customer_risk_score

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze revenue concentration: top 5 customers %, dependency risk and mitigation.

### sf_customer_satisfaction_trend

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer satisfaction scores over time with trend alerts and action triggers.

### sf_customer_segment_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define customer segments by rules (revenue, recency, industry) with membership refresh.

### sf_customer_segments_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define customer segmentation rules: RFM scores, tiers and assignment automation.

### sf_customer_visit_reports

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Field visit reports: agenda, findings, opportunities spotted, photos and next steps.

### sf_cycle_count_scheduler

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Schedule and run cycle counts per zone/ABC class with variance tracking and adjustment approval.

### sf_damaged_goods_log

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log damaged stock with cause, responsibility (internal/carrier/customer) and cost recovery.

### sf_data_dedup

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect duplicate partners (name, email, VAT) with similarity scoring, review groups and track merges

### sf_data_quality_check

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Run data quality checks: completeness, accuracy, consistency with scores.

### sf_deal_desk_request

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Complex deal reviews: pricing, terms, legal review with cross-functional approval.

### sf_debt_collection

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Aging analysis, collection cases, dunning plans and payment promises

### sf_decision_log

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Record important decisions: context, options considered, rationale, decision maker and review date.

### sf_demand_planning_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review demand forecast vs actual per product with bias tracking and parameter tuning.

### sf_digital_delivery

- **Models:** None
- **Depends:** base, mail, contacts, product, sale
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Digital products, automatic license key generation, expirable download links and digital delivery tracking

### sf_direct_print_pro

- **Models:** None
- **Depends:** base, stock, sale, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Print reports & labels directly to network/Bluetooth printers

### sf_disciplinary_action

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Disciplinary actions: type, date, description, follow-up and expiry.

### sf_dividend_register

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Declare dividends per shareholder meeting, track payment status and withholding.

### sf_dock_appointments

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Dock registry and truck appointment scheduling with time windows, arrival tracking and no-show detection

### sf_document_approval_hybrid

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Chase pending document approvals: who has it, since when, escalation after SLA.

### sf_document_expiry_tracker

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee document expiry with automated renewal reminders.

### sf_donations

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Donation campaigns, pledges, payments and fiscal receipts with automatic reminders

### sf_dr_plan_tracker

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** DR plans: RTO/RPO targets, last test date, next test and gaps.

### sf_dropship_operations

- **Models:** None
- **Depends:** base, sale, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track dropship orders: supplier notification, tracking collection and customer delivery status.

### sf_edi_einvoicing

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Peppol, Factur-X, ViDA, ANSI X12, CFDI, KSeF - certified e-invoicing & EDI

### sf_ehs_inspection_schedule

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Schedule EHS inspections per site/area with checklists, findings and corrective links.

### sf_emergency_purchase_log

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log emergency bypass purchases with retro-PO requirement and approval after the fact.

### sf_employee_1on1_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track regular 1-on-1 meetings: topics, feedback, development actions and mood.

### sf_employee_asset_return

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track company asset returns on exit: laptop, badge, phone with deposit release.

### sf_employee_engagement_action

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee engagement improvement actions from survey results.

### sf_employee_loans

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage employee loans and salary advances with auto repayment schedules

### sf_employee_referral

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee referrals: candidate, hiring stage, bonus eligibility and payment.

### sf_employee_skill_gap

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze skill gaps: required vs actual skills per role with training recommendations.

### sf_employee_survey

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pulse surveys: questions, participation rate, eNPS and action plans.

### sf_energy_meter_readings

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monthly meter readings per site with consumption trends and anomaly alerts.

### sf_energy_monitoring

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track energy and utility consumption per site and meter with ESG reporting

### sf_energy_saving_tracker

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track energy-saving initiatives: investment, savings, payback and CO2 reduction.

### sf_environmental_waste_tracking

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track waste streams per site: type, quantity, disposal method, cost and recycling rate.

### sf_equipment_rental

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Equipment cards with calendar availability, rental contracts with tiered pricing, out/in inspections, damages and planned maintenance

### sf_equipment_utilization

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track equipment utilization: available hours, used hours and OEE contribution.

### sf_esg_reporting

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Collect, validate and report ESG indicators (environment, social, governance) per company and period for CSRD compliance

### sf_events

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Events, sessions, speakers, registrations and ticketing, badge check-in, budget and revenue tracking

### sf_exit_interviews

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured exit interviews: reasons, destination, improvement feedback and action items.

### sf_expiry_alert_manager

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Expiry alerts per lot with FEFO compliance checks and write-off workflow.

### sf_export_documents

- **Models:** None
- **Depends:** base, mail, contacts, sale, product
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Export pack documents, Incoterms, completeness control and dossier workflow

### sf_external_audit_tracker

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track external audit findings: severity, owner, remediation plan and closure evidence.

### sf_facility_management

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sites, rooms and bookings with capacity control and conflict detection

### sf_field_dispatch_board

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Dispatch board with skills matching, route optimization, SLA timers and mobile check-in/out.

### sf_field_service_checklist

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mobile checklists for field service: pre-work, tasks, photos and customer signature.

### sf_field_service_customer_satisfaction

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Post-service customer satisfaction: rating, comments and follow-up for low scores.

### sf_field_service_dispatch

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Dispatch field technicians: skills matching, route optimization and SLA timers.

### sf_field_service_offline

- **Models:** None
- **Depends:** base, industry_fsm, stock, mail
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** True offline-first mobile app for field technicians with background sync

### sf_field_service_parts

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track parts used in field service: part, quantity, vehicle stock and restock needs.

### sf_financial_covenant_monitor

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor bank loan covenants (ratios vs thresholds) per period with breach alerts.

### sf_financial_ratio_dashboard

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compute key ratios (liquidity, solvency, profitability) from period data.

### sf_first_article_inspection

- **Models:** None
- **Depends:** base, quality, mrp, stock, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** First Article Inspection per AS9102/AS9145 for aerospace/automotive

### sf_first_piece_validation

- **Models:** None
- **Depends:** base, mrp, quality, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** First-piece validation per setup: measurements, checklist and production release gate.

### sf_fixed_asset_transfer

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Transfer assets between entities with valuation and journal entries.

### sf_fixed_assets

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Assets, categories, depreciation plans and lifecycle tracking

### sf_franchise

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Franchise contracts, declared sales, automatic royalty calculation, invoicing and payment tracking

### sf_freight_audit

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Audit carrier invoices against contracts and shipments: detect overcharges, manage disputes, recover money

### sf_freight_costing

- **Models:** None
- **Depends:** base, stock, account
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track carriers, cost formulas and freight on pickings

### sf_freight_quote_compare

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compare carrier quotes per shipment: transit, cost, surcharges with award decision.

### sf_fuel_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Fuel cards, fills with L/100km consumption tracking, tanks with receipts and anomaly alerts

### sf_fx_hedge_accounting

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Hedge accounting documentation: designation, effectiveness testing and entries.

### sf_fx_hedging

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Open FX exposure per currency from receivables/payables, forward contracts with settlement gain/loss tracking

### sf_fx_reval_scheduler

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monthly foreign currency revaluation proposals per currency with unrealized gain/loss computation.

### sf_gifts_hospitality

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Anti-bribery register of gifts and hospitality given or received with approval threshold

### sf_grants

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Grant programs, calls for projects, application workflow, justified expenses and financial reports

### sf_grievance_tracker

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Formal grievance cases: type, severity, investigation and resolution.

### sf_gym_fitness

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Gym memberships, plans, group classes, sessions, attendances and payments with automatic alerts

### sf_haccp

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** HACCP food safety: plans, CCP, critical limits, monitoring checks, deviations, corrective actions and auditable PDF registers

### sf_hotel_pms

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Hospitality & Reservations (light PMS)

### sf_hr_onboarding

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured onboarding and offboarding journeys with checklists, tasks and alerts

### sf_hse_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Incidents, inspections, risk assessments, work permits and PPE tracking

### sf_iatf_quality_suite

- **Models:** None
- **Depends:** base, quality, maintenance, mrp, stock, mail, product
- **Python Files:** 10
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, MSA, SPC

### sf_ic_netting

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Match open intercompany balances across entities, compute net positions per company pair and generate settlement entries

### sf_incident_oncall

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Escalation chains for incidents: L1->L2->L3 with timers and ack tracking.

### sf_incident_postmortem

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Operational incident reviews: severity, timeline, root cause, corrective actions and lessons library

### sf_insurance_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Insurance policies, premiums, guarantees, renewals and claims with indemnities

### sf_intercompany_balance_check

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monthly intercompany balance comparison per pair with discrepancy investigation.

### sf_intercompany_invoicing

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated intercompany invoices with multi-book accounting, currency conversion and elimination entries.

### sf_intercompany_loan

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** IC loans: principal, rate, schedule, interest postings and repayment tracking.

### sf_interim_billing_tracker

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track interim/progress invoicing on long projects: % complete, billed, remaining.

### sf_internal_audit_program

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Annual internal audit plan: scope, auditors, planned dates, status and findings links.

### sf_internal_mobility

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Post internal openings, manage applications from employees and transfer tracking.

### sf_internship_tracker

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Interns: school, duration, mentor, project and conversion status.

### sf_inventory_abc_classification

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Classify inventory by value and movement: A/B/C with counting frequency per class.

### sf_inventory_accuracy_rate

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track inventory accuracy per zone: counted, matched, IRA% and improvement actions.

### sf_inventory_aging

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Stock aging buckets from last movement, slow-mover detection and obsolescence provision suggestions

### sf_inventory_count_variance

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze count variances: product, zone, reason code and trend with root cause.

### sf_inventory_revaluation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track inventory revaluations: period, method, adjustment and accounting impact.

### sf_inventory_shrinkage_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track inventory shrinkage: theft, damage, administrative errors with cost impact.

### sf_inventory_turnover_analysis

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze inventory turnover per product/category with benchmark comparison.

### sf_inventory_writeoff_register

- **Models:** None
- **Depends:** base, stock, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Registered stock write-offs with approval, valuation impact and reason analytics.

### sf_investment_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Portfolios, investment lines, valuations, dividends and coupons, maturity alerts and PDF performance reports

### sf_invoice_discounting

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register factored/discounted invoices: advance %, fees, maturity and repurchase tracking.

### sf_invoice_matching

- **Models:** None
- **Depends:** base, sale, purchase, purchase_stock, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Automatic purchase order / receipt / invoice reconciliation with tolerances and exceptions

### sf_it_asset_lifecycle

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track IT assets: purchase, assignment, warranty expiry, refresh cycle and disposal.

### sf_it_asset_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track IT equipment, software licenses, assignments and warranties

### sf_it_capacity_planning

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track server/cloud capacity: CPU, RAM, storage utilization with threshold forecasts.

### sf_job_costing_snapshot

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Project/job cost snapshots: labor, materials, overheads vs budget with margin alerts.

### sf_key_account_plans

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Joint business plans per key account: objectives, actions, forecasts and review dates.

### sf_knowledge_articles

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Internal knowledge base articles with lifecycle: draft, reviewed, published, needs update.

### sf_kpi_target_register

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Central KPI register: definition, formula, owner, targets per period and actuals.

### sf_kyc_aml

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Customer due diligence register: risk rating, PEP/sanctions screening cycles, UBO declaration and periodic reviews

### sf_late_payment_interest

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compute late payment interest on overdue invoices per legal rate, generate interest invoices.

### sf_laundry

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Deposit vouchers and items, treatment statuses, per-piece pricing, pickup/delivery and customer history

### sf_lead_scoring_ai

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams.

### sf_lease_ifrs16

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Right-of-use assets, lease liabilities, PV schedules, monthly journal entries and modifications - IFRS 16 & ASC 842

### sf_library

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Catalogue, members, loans, returns, late fees and reservations with cron alerts

### sf_line_balancing_review

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review workstation cycle times vs takt time with imbalance flags and rebalancing actions.

### sf_litigation

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Legal cases and pre-litigation: cases and parties, domains, procedural deadlines with alerts, fees and honoraries, decisions and results, legal activity PDF report

### sf_load_planning

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Build truck loads from pickings with capacity checks (weight, volume, pallets), route stops and load manifest

### sf_maintenance_cost_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track maintenance costs per equipment: preventive, corrective, parts and labor.

### sf_maintenance_intake

- **Models:** None
- **Depends:** base, maintenance, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Internal maintenance request intake: priority triage, assignment and resolution feedback.

### sf_maintenance_schedule_optimizer

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Optimize maintenance schedules: equipment criticality, usage and production impact.

### sf_management_reporting

- **Models:** None
- **Depends:** base, account, sale, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Board-ready monthly pack: revenue, costs, margin KPIs vs previous month with commentary

### sf_marketing_budget_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track marketing budget per channel: allocated, spent, remaining and ROI per channel.

### sf_marketing_campaign_roi

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track marketing campaigns: spend, leads, conversions and ROI computation.

### sf_marketplace_hub

- **Models:** None
- **Depends:** base, sale, account, product
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Multi-vendor marketplace: channels, vendors, listings and orders in one hub

### sf_mcp_server_pro

- **Models:** None
- **Depends:** base, mail, sale, stock, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Connect AI assistants to your Odoo instance securely

### sf_medical_practice

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Patient files, conflict-free appointment agenda, consultations, prescriptions and vital signs with computed BMI

### sf_meeting_minutes

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Meeting minutes with decisions and action items: owners, due dates and completion tracking.

### sf_membership_advanced

- **Models:** None
- **Depends:** base, mail, sale, account, website
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage members, subscriptions & renewals for associations and NGOs

### sf_mental_health

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mental health practice: patient records, treatment plans, sessions, billing, outcomes

### sf_mes_andons

- **Models:** None
- **Depends:** base, mrp, stock, maintenance, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Real-time Andon alerts, escalation and response tracking for shop floor

### sf_mes_shop_floor

- **Models:** None
- **Depends:** base, mrp, stock, quality
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track work orders, stations, downtime and quality on the floor

### sf_mgmt_fee_billing

- **Models:** None
- **Depends:** base, account, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Bill recurring management fees (AUM %, fixed, per-hour) to related or external entities.

### sf_min_order_enforcement

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Minimum order value and quantity rules per customer segment with override approval.

### sf_minmax_review

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Periodic review workflow for min/max stock parameters with demand evidence and approval.

### sf_multi_site_price_harmony

- **Models:** None
- **Depends:** base, sale, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect price differences for the same product across sites/entities with harmonization workflow.

### sf_nonconformance_cost

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Calculate cost of non-conformance: rework labor, scrap material, delay penalties.

### sf_nps_feedback

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** NPS survey campaigns with automated detractor follow-up, trend analysis and team scorecards.

### sf_obsolescence_forecast

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Forecast obsolescence risk per product based on movement trends and lifecycle stage.

### sf_occupational_health

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Medical visits, aptitudes, restrictions, vaccinations and compliance dashboard

### sf_onboarding_cost

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track cost per new hire: recruiting, equipment, training and time to productivity.

### sf_oncall_schedule

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** On-call rotations with escalation levels, override tracking and handover notes.

### sf_ooo_calendar

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** OOO periods with backup assignment and handover notes, visible to teams.

### sf_operator_skill_matrix

- **Models:** None
- **Depends:** base, mrp, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Operator qualifications per workcenter/skill with levels, expiry and training needs.

### sf_order_freeze_windows

- **Models:** None
- **Depends:** base, sale, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Block order modifications during picking/invoicing windows with override approval.

### sf_overtime_preapproval

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pre-approve overtime before it happens: hours, project, budget check and post-validation.

### sf_packaging_consigns

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Returnable packaging consigns: deposit types, parks per site, emissions/returns linked to deliveries, invoiced deposits, return rate and stock alerts

### sf_packaging_spec_register

- **Models:** None
- **Depends:** base, product, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Packaging specs per product: box type, dimensions, labels, pallet config with revisions.

### sf_pallet_sscc_labels

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Generate SSCC-compliant pallet labels with GS1 codes linked to deliveries.

### sf_parking_management

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Parking sites and zones, spaces, recurring subscriptions, tickets, entry/exit and occupancy statistics

### sf_payment_milestone_engine

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define milestone-based payment terms on sales orders: percentages per milestone with due dates and tracking.

### sf_payroll_deadline_tracker

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Payroll calendar: input cutoff, processing, payment and declaration dates per month.

### sf_peak_season_planning

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Peak season readiness: staffing, stock build, carrier capacity and daily targets.

### sf_period_close

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Structured financial close: checklist templates, task orchestration, sign-offs, blockers and close calendar

### sf_pharmacy

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Pharmacy management: products, batches, expiries and prescription dispensations

### sf_po_acknowledgment

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier PO acknowledgments: sent, confirmed, late and escalation.

### sf_po_amendment_log

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log and approve purchase order amendments (qty, price, date) with before/after trace.

### sf_po_budget_check

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Check PO against budget before approval: budget line, available, over-budget routing.

### sf_policy_acknowledgment

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Versioned internal policies, employee assignment, acknowledgment sign-off, reminders and coverage rate

### sf_policy_exception_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track policy exceptions: policy, exception reason, risk, compensating controls and expiry.

### sf_policy_waivers

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Time-boxed policy waivers with risk assessment, compensating controls and approval workflow

### sf_prepaid_amortization

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track prepaid expenses (insurance, subscriptions, rent) with monthly amortization schedules.

### sf_preventive_maintenance_pro

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.

### sf_price_change_mgmt

- **Models:** None
- **Depends:** base, product, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan, announce and apply price increases: product lines with old/new price, delta %, effective dates and one-click application

### sf_price_matrix

- **Models:** None
- **Depends:** base, sale, product, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Tiered pricing and discount matrix per customer category

### sf_privacy_rgpd

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights management

### sf_probation_review_tracker

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Probation periods with review checkpoints, outcomes and confirmation workflow.

### sf_process_routing

- **Models:** None
- **Depends:** base, mrp, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Alternative routing selection based on conditions, capacity, and quality

### sf_procurement_savings_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track procurement savings: negotiated, implemented, annualized with initiative links.

### sf_product_compliance

- **Models:** None
- **Depends:** base, mail, product, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Regulatory compliance of products (CE, RoHS, REACH, UL, FDA): regulations, requirements, compliance dossiers and certificates with expiry alerts

### sf_product_eol

- **Models:** None
- **Depends:** base, product, sale, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping, open order checks and sale blocking

### sf_product_lifecycle_stage

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track products through lifecycle: introduction, growth, maturity, decline with strategies.

### sf_product_margin_matrix

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** ABC classification by margin and volume with pricing action recommendations.

### sf_product_pim

- **Models:** None
- **Depends:** base, product, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Central product data, families, attributes, completeness score and channel publications

### sf_product_return_rate

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor return rates per product with quality alerts above thresholds.

### sf_product_return_reasons

- **Models:** None
- **Depends:** base, sale, stock, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Coded product returns: reason tree, cost of returns and corrective action tracking.

### sf_product_reviews

- **Models:** None
- **Depends:** base, mail, product, sale, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Customer product reviews, moderation workflow, verified purchases and aggregated ratings

### sf_production_capacity_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capacity planning per workcenter: available hours, load, over/under capacity.

### sf_production_capacity_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Weekly capacity review: workcenter loads, bottlenecks and action items.

### sf_production_capacity_whatif

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze capacity what-if scenarios: new orders, machine downtime, overtime options.

### sf_production_downtime_pareto

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pareto analysis of production downtime: reasons, minutes, cost and cumulative ranking.

### sf_production_line_efficiency

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor line efficiency: planned time, downtime, ideal vs actual cycle time.

### sf_production_meeting_actions

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Daily production meeting: attendance, topics, action items with owners and due dates.

### sf_production_oee_calculator

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Calculate OEE: availability x performance x quality with loss analysis.

### sf_production_oee_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure OEE dashboards: metrics, targets, thresholds and alert rules.

### sf_production_oee_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track OEE: availability x performance x quality with loss breakdown.

### sf_production_order_priority

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage production order priorities: urgency, customer importance and sequencing.

### sf_production_order_sequencing

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sequence production orders: priority, changeover time, due dates and optimization.

### sf_production_planning

- **Models:** None
- **Depends:** base, mail, mrp
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Master production schedule with Gantt, priorities and work center load

### sf_production_scenarios

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Model production scenarios: capacity changes, rush orders and material shortages.

### sf_production_schedule_alert

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect schedule variances: planned vs actual dates with root cause coding.

### sf_production_scheduling

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Finite capacity scheduling with Gantt view, bottleneck detection and what-if simulation.

### sf_production_scrap_analytics

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze production scrap: reasons, quantities, cost impact and reduction targets.

### sf_production_scrap_pareto

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pareto analysis of production scrap: reasons, quantities, cost and cumulative ranking.

### sf_production_trial_tracking

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track trial runs before series production: parameters, results and go/no-go decisions.

### sf_production_waste_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track production waste: material, energy, time with cost and reduction targets.

### sf_production_yield_analysis

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze production yield: planned vs actual, scrap reasons and improvement actions.

### sf_production_yield_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track production yield: planned qty, good qty, scrap qty with yield % and trend.

### sf_project_change_request

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Change requests on projects: scope change, cost impact, schedule impact and approval.

### sf_project_charter

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Project charters: objectives, scope, stakeholders, budget and approval.

### sf_project_lessons_learned

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capture lessons learned per project: what went well, what to improve, recommendations.

### sf_project_margin

- **Models:** None
- **Depends:** base, project, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track project budgets, costs and margins live

### sf_project_milestone_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track project milestones: planned vs actual dates, deliverables and sign-off.

### sf_project_portfolio_board

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Portfolio-level view of projects: status, budget, risk and resource allocation.

### sf_project_resource_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Allocate resources to projects: allocation %, period and over-allocation alerts.

### sf_project_risk_log

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Per-project risk log: probability x impact scoring, mitigation plans and review dates.

### sf_project_stakeholder

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Stakeholder register: influence, interest, engagement strategy and communication plan.

### sf_promotional_pricing_engine

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Time-based promotional pricing with customer segments, volume tiers and margin protection rules.

### sf_provision_register

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track legal, commercial and tax provisions per period with reversal and utilization tracking.

### sf_psa

- **Models:** None
- **Depends:** base, sale, project, hr, account, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage engagements, resources and time for services teams

### sf_purchase_approval_matrix

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Amount-based PO approval routing: thresholds, approvers per level with delegation.

### sf_purchase_contract_compliance

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Check purchase compliance: invoice prices vs contract prices, SLA adherence.

### sf_purchase_envelope

- **Models:** None
- **Depends:** base, purchase, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Annual purchase envelopes per category: budget, committed, consumed and remaining.

### sf_purchase_order_aging

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor open PO aging: days open, supplier, expected receipt and delay alerts.

### sf_purchase_price_analysis

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** PPV per product/vendor vs standard cost from posted bills, price change history and increase alerts

### sf_purchase_requisition

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Purchase requisition with multi-level approval chains, budget checking and vendor suggestion.

### sf_purchase_requisition_analytics

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze purchase requisitions: approval time, rejection rate and top requesters.

### sf_purchase_requisition_template

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Template-based purchase requisitions: pre-approved items, default vendors, budget codes.

### sf_qms_iso9001

- **Models:** None
- **Depends:** base, quality, maintenance, mrp, hr, documents
- **Python Files:** 17
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Full ISO 9001 QMS: NC/CAPA, audits, docs, FMEA, training, management review

### sf_quality_alert_aging

- **Models:** None
- **Depends:** base, quality, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor open quality alerts by age with escalation at thresholds.

### sf_quality_alert_auto_assign

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Auto-assign quality alerts based on product, defect type and team workload.

### sf_quality_alert_escalation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define quality alert escalation: severity levels, timers and notification chains.

### sf_quality_audit_program

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Annual quality audit program: scope, auditor, planned dates, findings and CAPA links.

### sf_quality_coa

- **Models:** None
- **Depends:** base, stock, quality, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow

### sf_quality_cost_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track cost of quality: prevention, appraisal, internal failure and external failure.

### sf_quality_document_control

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Version-controlled quality documents: SOPs, work instructions with review and approval.

### sf_quality_document_control_sys

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Version-controlled quality documents with review cycles and approval workflow.

### sf_quality_hold_register

- **Models:** None
- **Depends:** base, stock, quality, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register quality holds: stock blocked pending investigation with release/scrap decisions.

### sf_quality_inspection

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mobile-first quality inspection checklists with photo capture and non-conformance escalation.

### sf_quality_inspection_mobile2

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure mobile quality inspections: checklists, photos, offline mode and sync.

### sf_quality_inspection_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define inspection plans: operations, sampling, criteria and control method per product.

### sf_quality_inspection_planner

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan quality inspections per product/operation: sampling plan, frequency and criteria.

### sf_quality_pareto_analyzer

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Pareto analysis of defect types: count, cost, cumulative % and priority ranking.

### sf_quality_pareto_update

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monthly NC Pareto: types, counts, cost and cumulative ranking for quality reviews.

### sf_quality_trend_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure quality trend dashboards: metrics, targets, thresholds and alert rules.

### sf_quote_followup_cadence

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated follow-up cadence on quotations: D+3, D+7, D+14 tasks with outcome tracking.

### sf_real_estate

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Properties, leases, tenants and rent invoicing in one place

### sf_receiving_discrepancy_log

- **Models:** None
- **Depends:** base, stock, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log receipt discrepancies (qty, damage, wrong item) with disposition and supplier notification.

### sf_recurring_cost_register

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track all recurring costs: subscriptions, leases, insurance with renewal dates.

### sf_recurring_revenue_register

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register recurring revenue lines per customer: MRR, churned MRR, expansion tracking.

### sf_recurring_task_templates

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define recurring task sets (weekly checks, monthly reviews) with instance generation tracking.

### sf_regulatory_watch

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Register upcoming regulations: impact analysis, readiness assessment and action plans.

### sf_remote_work_requests

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Remote/telework requests with manager approval, days quota and equipment checklist.

### sf_renewal_management

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Renewal pipeline for customer contracts: notice deadlines, auto-renew flags, churn risk and renewal outcomes

### sf_rental_billing

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Recurring rental billing: contracts, automatic invoicing cycles, proration, deposit management.

### sf_replenishment_review

- **Models:** None
- **Depends:** base, stock, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review queue for reorder proposals: demand check, approval and order emission tracking.

### sf_resource_planning

- **Models:** None
- **Depends:** base, project, hr, resource
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Allocate resources to projects, track capacity and avoid overload

### sf_restaurant

- **Models:** None
- **Depends:** base, mail, contacts, product
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Restaurant and cafe management: tables, reservations, menus, kitchen orders and revenue tracking

### sf_retention_schedule

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Retention rules per document type: legal duration, disposal method and review workflow.

### sf_return_to_vendor

- **Models:** None
- **Depends:** base, stock, purchase, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Defective and excess goods returns to suppliers: RTV orders with dispositions (return/credit/replace/scrap), return pickings and debit note tracking

### sf_returns_rma

- **Models:** None
- **Depends:** base, sale, stock, account, delivery
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Unified returns portal for eCommerce, POS, B2B, marketplaces with auto-approval rules

### sf_revenue_backlog_tracker

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track signed-but-not-invoiced revenue backlog with expected invoicing months.

### sf_revenue_leak_detector

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect revenue leaks: unbilled services, expired discounts, missed escalations.

### sf_revenue_leakage_analyzer

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect revenue leakage: unbilled services, expired discounts, missed escalations.

### sf_revenue_milestone

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track revenue recognition milestones per contract with percentage completion.

### sf_revenue_protection_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Identify at-revenue-risk accounts with protection actions and owner assignment.

### sf_revenue_recognition

- **Models:** None
- **Depends:** base, account, sale, account_asset
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** ASC 606 / IFRS 15 compliant revenue recognition for subscriptions and contracts

### sf_rework_management

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Track rework orders, operations and scrap with cost computation and escalation alerts

### sf_risk_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Risk register, 5x5 matrix, treatment plans, controls and regulatory mapping

### sf_runbook_library

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Versioned operational procedures with review dates, owners and step checklists.

### sf_safety_inspections

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Schedule safety inspections per area with checklists, findings and corrective tracking.

### sf_safety_stock

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Optimal safety stock levels and reorder points from real demand

### sf_safety_training_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track mandatory safety training per employee with expiry and compliance rate.

### sf_sale_auto_workflow

- **Models:** None
- **Depends:** base, sale, stock, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automate quotes, deliveries and invoices with configurable rules

### sf_sales_asset_library

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Central library of sales assets: decks, one-pagers, case studies with version control.

### sf_sales_battle_rhythm

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Weekly sales rhythm: Monday pipeline, Wednesday coaching, Friday forecast with checklists.

### sf_sales_battlecard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Battle cards per competitor: strengths, weaknesses, win strategies and proof points.

### sf_sales_capacity_model

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Model sales capacity: ramp time, productivity per rep, coverage ratio and hiring plan.

### sf_sales_coaching_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Coaching dashboard per rep: pipeline health, activity metrics and skill gaps.

### sf_sales_coaching_effectiveness

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Measure coaching effectiveness: pre/post performance, skill improvement and ROI.

### sf_sales_coaching_log

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log coaching sessions per rep: topic, feedback, improvement area and next check-in.

### sf_sales_coaching_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured coaching plans per rep: skills assessment, development areas and milestones.

### sf_sales_commission

- **Models:** None
- **Depends:** base, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Flexible commission plans, auto-computed from paid invoices and tracked per salesperson

### sf_sales_commission_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Build commission plans: base rate, accelerators, bonuses, caps and clawbacks per team.

### sf_sales_commission_simulation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Simulate commission payouts under different plans: base, tiered, accelerator models.

### sf_sales_commission_statement

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Generate commission statements: deals, rates, calculations, deductions and totals.

### sf_sales_content_library

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Organize sales collateral: battle cards, case studies, ROI calculators with usage tracking.

### sf_sales_enablement_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track sales enablement: content used, training completed, certification and win rate impact.

### sf_sales_forecast_accuracy

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compare forecast vs actual sales per period with accuracy scoring and bias detection.

### sf_sales_forecast_category

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage forecast categories: commit, best case, pipeline with rules and accuracy tracking.

### sf_sales_gamification

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define gamification: badges, leaderboards, challenges with rewards.

### sf_sales_hiring_funnel

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track sales hiring funnel: applications, interviews, offers and ramp progress.

### sf_sales_hiring_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan sales hiring: headcount, ramp schedule, expected productivity and cost per hire.

### sf_sales_hiring_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track sales hiring: candidates, ramp progress, quota attainment and time to full productivity.

### sf_sales_huddle_notes

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Daily sales huddle: wins, blockers, priorities and team morale tracking.

### sf_sales_hygiene_audit

- **Models:** None
- **Depends:** base, sale, crm, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect stale opportunities, missing next steps and overdue closing dates with cleanup campaigns.

### sf_sales_onboarding_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured sales onboarding: product training, shadow calls, certification and first deal.

### sf_sales_order_acknowledgment

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track customer order acknowledgments (OA) required by customers with delay alerts.

### sf_sales_pipeline_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Weekly pipeline review: stage movements, stuck deals, forecast changes and actions.

### sf_sales_play_execution

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track execution of sales plays: play used, target accounts, results and effectiveness.

### sf_sales_playbook

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured sales plays: triggers, steps, templates and success metrics.

### sf_sales_routes

- **Models:** None
- **Depends:** base, sale, crm
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan field sales routes, track visits, territories and objectives

### sf_sales_target_cascade

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Cascade annual targets to quarterly and monthly with rep-level breakdown.

### sf_sales_territory_planner

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan sales territories: geographic zones, account distribution and workload balance.

### sf_sales_territory_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review territory workload balance: accounts, revenue potential and rep capacity.

### sf_salon_beauty

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Appointments, staff availability, packages, commissions and billing for salons and beauty studios

### sf_sample_management

- **Models:** None
- **Depends:** base, sale_management, stock, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sample requests to prospects/customers: approval, shipment, feedback and conversion tracking with full cost visibility

### sf_school_management

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 16
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Students, groups/classes, teachers, courses, absences, grades, report cards and tuition fee management

### sf_scrap_reason_analytics

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Coded scrap with reason tree, Pareto analysis and improvement action tracking.

### sf_sell_through_reporting

- **Models:** None
- **Depends:** base, sale, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Collect monthly sell-through and stock levels from distributors, compute weeks of channel stock.

### sf_senior_living

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 20
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Complete management for senior residences, EHPAD, retirement communities

### sf_service_catalog

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Catalog of internal services: description, request types, SLA, owner and fulfillment steps.

### sf_service_contracts

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Service contracts, SLA tiers and breach tracking

### sf_service_level_agreement_monitor

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor internal service level agreements between departments with breach tracking.

### sf_shift_swap_board

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Employees post and accept shift swaps with manager approval.

### sf_shop_floor_terminal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shop floor terminal for work order tracking, time logging, quantity reporting and scrap entry.

### sf_sla_pause_tracking

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track SLA clock pauses (waiting for customer, change freeze) with pause/resume timestamps.

### sf_software_license_renewals

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** License subscriptions with renewal dates, costs, seats and auto-renewal risk flags.

### sf_spa_wellness

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 27
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Complete spa management: resource planning, therapists, treatments, packages, memberships

### sf_spare_parts_minmax

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Critical spare parts min/max with supplier lead times and stockout risk alerts.

### sf_special_price_approval

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Discount requests beyond thresholds with margin impact, approver chain and validity.

### sf_spend_analytics

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Spend per vendor and category from posted bills, PO coverage and maverick buying detection

### sf_staffing

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Temporary work and placement agency management: candidates, clients, needs, missions, contracts, timesheets and invoicing.

### sf_stock_adjustment_approval

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Approval workflow for inventory adjustments above thresholds with reason codes.

### sf_stock_barcode_advanced

- **Models:** None
- **Depends:** base, stock, product
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Advanced barcode scanning for inventory operations

### sf_store_credit

- **Models:** None
- **Depends:** base, mail, contacts, sale
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Customer store credit accounts, reusable credit grants, usage, adjustments, expirations and balances

### sf_subscription_dunning

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated dunning: retry schedules, escalation emails and revenue recovery dashboard.

### sf_succession_plan

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Key position succession: candidates, readiness and development actions.

### sf_supplier_audit_program

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Annual supplier audit program: risk-based scheduling, scope and findings.

### sf_supplier_audit_scheduler

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan supplier audits: risk-based frequency, scope, findings and follow-up.

### sf_supplier_bank_change_alert

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Fraud-control workflow for supplier bank detail changes: dual verification before payment.

### sf_supplier_capacity_check

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Verify supplier capacity before large orders: capacity, current load, confirmation workflow.

### sf_supplier_capacity_forecast

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Forecast supplier capacity vs our demand by month with shortage alerts.

### sf_supplier_capacity_planner

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan supplier capacity: current load, available capacity and expansion needs.

### sf_supplier_capacity_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review supplier capacity: current load, available capacity, lead time impact and risks.

### sf_supplier_contract_database

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Central database of supplier contracts: terms, values, renewals and key clauses.

### sf_supplier_contract_renewal

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier contract renewals: expiry, performance review and renegotiation.

### sf_supplier_contract_renewal_alert

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Alert system for supplier contract renewals: days-to-expiry tracking and action items.

### sf_supplier_contract_renewal_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier contract renewals: expiry timeline and renegotiation status.

### sf_supplier_diversity_tracker

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier diversity: categories, spend %, goals and progress reporting.

### sf_supplier_invoice_3way_match

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor 3-way matches: PO vs receipt vs invoice with tolerances and exceptions.

### sf_supplier_invoice_3way_match3

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure invoice matching rules: tolerance levels, auto-match criteria and exceptions.

### sf_supplier_invoice_accuracy

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier invoice errors: price mismatches, qty issues with error rate KPI.

### sf_supplier_invoice_matching

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure invoice matching rules: tolerance levels, auto-match criteria and exceptions.

### sf_supplier_leadtime_audit

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compare quoted vs actual lead times per supplier with trend and rating.

### sf_supplier_negotiation_prep

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Prepare supplier negotiations: leverage points, targets, BATNA and strategy.

### sf_supplier_onboarding_checklist

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured supplier onboarding: documents, quality audit, trial order and approval.

### sf_supplier_onboarding_portal

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure supplier onboarding portal: required documents, forms and approval steps.

### sf_supplier_pareto_abc

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Classify suppliers by spend and criticality: A/B/C with review frequency per class.

### sf_supplier_payment_optimization

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Optimize supplier payment timing: early payment discounts vs cash preservation.

### sf_supplier_payment_terms

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze supplier payment terms vs actual payment behavior with optimization tips.

### sf_supplier_performance_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure supplier performance dashboards: KPIs, thresholds and alert rules.

### sf_supplier_performance_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Quarterly supplier review: scorecard, improvement actions and relationship notes.

### sf_supplier_pricing_benchmark

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Benchmark supplier prices: current vs market, savings opportunities and actions.

### sf_supplier_pricing_history

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track supplier price changes over time with trend analysis and alerts.

### sf_supplier_pricing_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Annual supplier pricing review: current prices, market benchmark, negotiation targets.

### sf_supplier_pricing_tiers

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Volume-based pricing tiers per supplier: thresholds, discounts and savings calculation.

### sf_supplier_questionnaire

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Send compliance/ESG questionnaires to suppliers with response tracking and scoring.

### sf_supplier_rebates

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking

### sf_supplier_risk_dashboard

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure supplier risk dashboard: risk categories, weights, thresholds and alerts.

### sf_supplier_risk_mitigation

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mitigation plans for supplier risks: dual sourcing, inventory buffer, contract clauses.

### sf_supplier_risk_mitigation_plan

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mitigation plans for supplier risks: dual sourcing, buffer stock, contract clauses.

### sf_supplier_risk_register

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Supplier risk scoring: financial, geographic, single-source and compliance risks with mitigation.

### sf_supplier_risk_score

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Score supplier risks: financial, geographic, single-source and compliance factors.

### sf_supplier_scorecard

- **Models:** None
- **Depends:** base, purchase, stock, quality
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Score suppliers on delivery, quality and compliance

### sf_supplier_scorecard_review

- **Models:** None
- **Depends:** base, purchase, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Quarterly supplier review meetings: scores, action plans and improvement commitments.

### sf_system_health_check

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Daily system health checks: database size, disk space, active users, response time.

### sf_tax_deadline_calendar

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Fiscal obligation calendar: VAT, corporate tax, payroll deadlines with reminders and responsible assignment.

### sf_tax_provision_calc

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Compute deferred/current tax provisions with temporary difference tracking.

### sf_telecom_expense

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mobile/data/landline lines per employee, plan costs and monthly invoice variance audit

### sf_telework_policy

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Telework policy rules, eligibility, day quotas and compliance tracking.

### sf_tender_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage RFQ/RFI/RFP and public tenders with criteria scoring and justified award

### sf_territory_mapping

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Assign territories to reps with zip/postal code ranges and account lists.

### sf_third_party_risk

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Assess third-party risks: vendor, data access, criticality and mitigation plan.

### sf_tiktokshop_connector

- **Models:** None
- **Depends:** base, sale, stock, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sync products, orders and stock with TikTok Shop

### sf_time_attendance

- **Models:** None
- **Depends:** base, hr, hr_attendance, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shifts, overtime, late arrivals and attendance analytics

### sf_tool_management

- **Models:** None
- **Depends:** base, mrp, stock, maintenance, quality
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track tools, gauges, fixtures with calibration, wear, and lifecycle

### sf_tooling_request

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request tooling preparation per production order: tools needed, readiness status and delays.

### sf_traceability

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Full batch traceability, recall events and product history

### sf_trade_finance

- **Models:** None
- **Depends:** base, sale, purchase, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Letters of credit, bank guarantees and documentary collections with key dates and documents

### sf_trade_promotions

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Trade promotion programs, budgets, customer claims, validation workflow and ROI tracking

### sf_training_budget

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Training budget per department: allocated, spent, remaining and ROI.

### sf_training_certifications

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee trainings, sessions, registrations and certifications with expiry alerts

### sf_training_feedback

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Collect structured feedback per training session: ratings, comments and improvement actions.

### sf_transfer_pricing

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Intercompany arm-length pricing policies (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation

### sf_travel_agency

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Manage travel packages, providers, reservations and margin analysis.

### sf_treasury_week_board

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Weekly cash planning: expected inflows/outflows per day with balance projection and decisions.

### sf_upsell_trigger_rules

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Define upsell triggers: usage threshold, contract end proximity, feature gaps.

### sf_user_activity_log

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Daily user activity summary: logins, actions per module, and anomaly detection.

### sf_utility_billing

- **Models:** None
- **Depends:** base, mail, uom, contacts, account
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Delivery points and meters registry, reading campaigns, tiered tariffs and consumption invoices

### sf_vehicle_workshop

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vehicles, intervention requests, repair orders with operations and parts, full cost per vehicle and urgency alerts

### sf_vendor_contracts

- **Models:** None
- **Depends:** base, product, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage supplier contracts, clauses, amounts, expirations and renewals with alerts

### sf_vendor_onboarding_portal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vendor onboarding portal with document collection, compliance verification and approval workflow.

### sf_vendor_portal

- **Models:** None
- **Depends:** base, purchase, portal, account, mail
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Self-service vendor portal: RFQs, quotations, orders and invoices online

### sf_vendor_sample_tracking

- **Models:** None
- **Depends:** base, purchase, product, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Request and track samples from suppliers: request, received, evaluated, approved for use.

### sf_vendor_scorecard_auto

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Auto-compute vendor scores from delivery, quality and invoice data with trends.

### sf_vendor_sla_monitor

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor supplier SLAs: response/resolution targets vs actuals with breach logging.

### sf_veterinary

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Veterinary clinic management: animal patients, appointments, vaccinations and hospitalizations

### sf_visitor_access

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Visitor check-in/out, badges, zones, safety rules and real-time presence register

### sf_warehouse_heatmap

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Activity heatmap for slotting optimization: pick frequency, travel distance and ABC classification.

### sf_warehouse_layout_planner

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan warehouse layout: zones, aisles, rack positions with capacity and accessibility.

### sf_warehouse_safety_log

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Log warehouse safety incidents: type, severity, root cause and corrective actions.

### sf_warehouse_slotting_review

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Review product slotting: velocity, weight, size vs current location with move recommendations.

### sf_warehouse_throughput

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track daily throughput: orders picked, lines picked, errors and productivity per operator.

### sf_warehouse_throughput_daily

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Daily warehouse throughput: orders, lines, picks per hour and error rates.

### sf_warning_letter_register

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Formal warning letters: reason, severity, acknowledgment and expiry tracking.

### sf_warranty_claims_portal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Customer self-service warranty claims with SLA tracking and automatic credit note.

### sf_warranty_cost_analytics

- **Models:** None
- **Depends:** base, account, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Analyze warranty costs per product/supplier: claims, recovery and quality signals.

### sf_warranty_management

- **Models:** None
- **Depends:** base, mail, product, stock, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Product warranties, claims with automatic eligibility check and motivated decisions

### sf_waste_management

- **Models:** None
- **Depends:** base, mail, contacts, web
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Waste tracking slips (BSD), sites and waste codes

### sf_waste_stream_tracker

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track waste streams per site: type, quantity, disposal cost and recycling rate.

### sf_wave_picking

- **Models:** None
- **Depends:** base, stock, stock_picking_batch, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Group pickings into waves and release them efficiently

### sf_whatsapp_cloud_api

- **Models:** None
- **Depends:** base, mail, sale, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Send WhatsApp messages from Odoo via Meta Cloud API

### sf_win_loss_analysis

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured win/loss records: reasons, competitor, price gap and lessons for the sales team.

### sf_workorder_handover

- **Models:** None
- **Depends:** base, mrp, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured shift handover per workcenter: running orders, issues, watch-outs for the next shift.

### sf_yard_management

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 10
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Yard management: trailer inventory with dwell clocks, gate check-in/out, dock assignment, jockey shunts, detention billing

### sf_youth_sports

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Youth sports club: registrations, teams, seasons, matches, certificates, family portal

### sf_zone_capacity_monitor

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 4
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Monitor occupancy per warehouse zone with max capacity alerts and relocation suggestions.

