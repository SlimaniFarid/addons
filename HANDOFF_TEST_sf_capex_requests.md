# HANDOFF TEST — sf_capex_requests

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_capex_requests\`

## 🎯 Features to Test
- Multi-level approvals with auto-advance to Approved
- Rejection flow works
- Payback computed from annual benefit
- Lifecycle transitions enforced

## 🧪 Workflow Scenario
- Create request with business case and approval chain.
- Submit -> approve level by level.
- Mark Ordered (PO ref) -> Capitalized (asset ref).

## ⚠️ Watch Points
- Approval chain must be defined before submit.
- Request frozen after submission (by design).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_capex_requests to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- multi-level approvals with auto-advance to approved
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
