# HANDOFF TEST — sf_change_requests

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_change_requests\`

## 🎯 Features to Test
- Rollback gate
- Vote percentage
- Decision flow
- PIR section

## 🧪 Workflow Scenario
- Submit (rollback plan mandatory).
- CAB review with votes; close CAB decides.
- Implement, review, close or fail.

## ⚠️ Watch Points
- Submission blocked without rollback plan.
- CAB close: <50% approval = rejected.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_change_requests to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- rollback gate
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
