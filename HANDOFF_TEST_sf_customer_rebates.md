# HANDOFF TEST — sf_customer_rebates

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_customer_rebates\`

## 🎯 Features to Test
- Accrual math per type
- Category scoping
- Sales totals from invoices
- Settlement flow

## 🧪 Workflow Scenario
- Record deal (customer, period, type).
- Activate, compute accruals monthly.
- Settle with credit note reference.

## ⚠️ Watch Points
- Recompute deletes unclaimed accruals.
- Turnover bonus accrues 0 until threshold logic added in v1.1.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, sale, product, mail
Install: `Copy sf_customer_rebates to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- accrual math per type
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
