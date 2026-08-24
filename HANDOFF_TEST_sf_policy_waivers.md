# HANDOFF TEST — sf_policy_waivers

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_policy_waivers\`

## 🎯 Features to Test
- Date constraint
- Approval workflow
- Expiry flag computation
- Rejection reason gate

## 🧪 Workflow Scenario
- Request waiver (policy, reason, risk, controls, window).
- Approve or reject with reason.
- Track expiry flag.

## ⚠️ Watch Points
- valid_to must be >= valid_from (constraint).
- Rejection requires reason.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_policy_waivers to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- date constraint
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
