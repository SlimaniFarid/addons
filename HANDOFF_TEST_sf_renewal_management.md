# HANDOFF TEST — sf_renewal_management

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_renewal_management\`

## 🎯 Features to Test
- Deadline computation
- Expiring flag
- Renewed/lost outcomes
- Kanban by state

## 🧪 Workflow Scenario
- Log contracts (customer, type, term, notice period, value).
- Track notice/expiry countdowns.
- Flag expiring, renew or mark lost.

## ⚠️ Watch Points
- Notice deadline = end_date - notice_period_days.
- Renewed requires renewed_end_date (auto +1 year if empty).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, sale, mail
Install: `Copy sf_renewal_management to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- deadline computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
