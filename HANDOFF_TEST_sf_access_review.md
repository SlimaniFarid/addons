# HANDOFF TEST — sf_access_review

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_access_review\`

## 🎯 Features to Test
- Line generation with groups summary
- Decisions recorded
- Close gate
- Admin scope filter

## 🧪 Workflow Scenario
- Create campaign (scope, due date).
- Generate review lines per user.
- Keep/revoke each, close when all decided.

## ⚠️ Watch Points
- Close blocked while pending reviews.
- Admin scope filters group_system users.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_access_review to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- line generation with groups summary
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
