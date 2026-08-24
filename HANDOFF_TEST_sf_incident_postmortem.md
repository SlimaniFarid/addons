# HANDOFF TEST — sf_incident_postmortem

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_incident_postmortem\`

## 🎯 Features to Test
- Duration computation
- Action tracking
- State flow
- Lessons section

## 🧪 Workflow Scenario
- Log incident (severity, category, detection time).
- Analyze impact/root cause.
- Add actions, capture lessons, close.

## ⚠️ Watch Points
- Duration computed only when resolved_at set.
- Close allowed with open actions (soft gate).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_incident_postmortem to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- duration computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
