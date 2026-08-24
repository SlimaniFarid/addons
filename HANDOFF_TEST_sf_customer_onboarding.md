# HANDOFF TEST — sf_customer_onboarding

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_customer_onboarding\`

## 🎯 Features to Test
- Template to tasks generation
- Progress %
- Completion gate
- First order link

## 🧪 Workflow Scenario
- Build template steps.
- Start onboarding per customer (tasks generated).
- Complete tasks, then complete onboarding.

## ⚠️ Watch Points
- Complete blocked until all tasks done.
- Tasks generated once.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, sale, mail
Install: `Copy sf_customer_onboarding to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- template to tasks generation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
