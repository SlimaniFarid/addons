# HANDOFF TEST — sf_transfer_pricing

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_transfer_pricing\`

## 🎯 Features to Test
- Policy CRUD with validity and method params
- Variance computation on analysed transactions
- Review workflow with sign-off
- Documentation register with status workflow

## 🧪 Workflow Scenario
- Create a policy per entity pair (method, markup, validity).
- Review flagged transactions in Transaction Analysis.
- Maintain Master/Local File documentation per fiscal year.

## ⚠️ Watch Points
- CUP requires manual benchmark price (computed_alp = 0) - enter external benchmark.
- Scan of invoices is manual per policy in v1 (roadmap: auto-scan cron).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, mail
Install: `Copy sf_transfer_pricing to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- policy crud with validity and method params
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
