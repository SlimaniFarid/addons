# HANDOFF TEST — sf_management_reporting

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_management_reporting\`

## 🎯 Features to Test
- Revenue/costs/margin correct
- Prev-month delta
- KPI lines with delta
- Finalize gate

## 🧪 Workflow Scenario
- Create report (month period).
- Compute KPIs from posted entries.
- Add KPI lines and commentary, finalize.

## ⚠️ Watch Points
- KPIs from posted invoices/bills only.
- Final state freezes editing.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, sale, purchase, mail
Install: `Copy sf_management_reporting to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- revenue/costs/margin correct
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
