# HANDOFF TEST — sf_credit_insurance

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_credit_insurance\`

## 🎯 Features to Test
- Policy CRUD
- Buyer decision workflow
- Indemnity computation
- Claim settlement states

## 🧪 Workflow Scenario
- Record policy (insurer, coverage, period).
- Request buyer limits; record decisions.
- File claims; indemnity computed; track settlement.

## ⚠️ Watch Points
- Indemnity = claimed x buyer coverage %.
- Buyer approval requires approved_limit for reduced state.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, mail
Install: `Copy sf_credit_insurance to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- policy crud
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
