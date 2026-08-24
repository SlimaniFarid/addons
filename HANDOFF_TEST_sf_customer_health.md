# HANDOFF TEST — sf_customer_health

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_customer_health\`

## 🎯 Features to Test
- Signal computation from orders/invoices
- Score within 0-100
- Risk mapping
- Kanban by risk

## 🧪 Workflow Scenario
- Register key accounts.
- Refresh signals (revenue, recency, overdue).
- Work at-risk customers first.

## ⚠️ Watch Points
- Score = recency(40) + trend(35) + overdue(25).
- Overdue > 0 forces at_risk minimum.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, sale, account, mail
Install: `Copy sf_customer_health to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- signal computation from orders/invoices
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
