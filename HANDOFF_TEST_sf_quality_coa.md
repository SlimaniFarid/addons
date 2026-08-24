# HANDOFF TEST — sf_quality_coa

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_quality_coa\`

## 🎯 Features to Test
- Prefill from picking
- All-pass gate
- Workflow states
- Tester/approver sign-off

## 🧪 Workflow Scenario
- Create CoA per delivery (product/lot prefilled).
- Enter test results and verdicts.
- Tested -> Approved (all-pass gate) -> Issued.

## ⚠️ Watch Points
- Approval blocked if any parameter fails.
- PDF certificate layout on roadmap.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, stock, quality, mail
Install: `Copy sf_quality_coa to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- prefill from picking
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
