# HANDOFF TEST — sf_telecom_expense

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_telecom_expense\`

## 🎯 Features to Test
- Expected computation
- Variance % and alert
- Contract-end flags
- Review state

## 🧪 Workflow Scenario
- Register lines (employee, provider, plan cost).
- Audit invoices: expected vs invoiced.
- Investigate variances beyond tolerance.

## ⚠️ Watch Points
- Expected = sum active line costs for provider.
- hr.employee used for assignment.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_telecom_expense to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- expected computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
