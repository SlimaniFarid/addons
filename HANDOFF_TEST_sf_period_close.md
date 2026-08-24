# HANDOFF TEST — sf_period_close

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_period_close\`

## 🎯 Features to Test
- Template -> tasks generation with computed due dates
- Progress % correct (NA excluded)
- Close validation blocks on open tasks
- Sign-offs recorded with user and date

## 🧪 Workflow Scenario
- Create checklist template (steps per department).
- Open Close Period: dates + template -> Generate Tasks.
- Work tasks to Done/NA, resolve blockers, Close.

## ⚠️ Watch Points
- Close blocked until every task is Done or N/A (by design).
- action_block sets the period to Blocked - reset tasks to clear.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, mail
Install: `Copy sf_period_close to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- template -> tasks generation with computed due dates
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
