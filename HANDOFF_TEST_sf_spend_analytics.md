# HANDOFF TEST — sf_spend_analytics

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_spend_analytics\`

## 🎯 Features to Test
- Spend totals match bills
- PO split correct
- Maverick alerts
- Recompute clean

## 🧪 Workflow Scenario
- Create run (period, tolerance).
- Compute from posted bills.
- Review maverick vendors beyond tolerance.

## ⚠️ Watch Points
- Maverick = bill lines without purchase_line_id.
- Credit notes excluded in v1.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, purchase, product, mail
Install: `Copy sf_spend_analytics to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- spend totals match bills
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
