# HANDOFF TEST — sf_kyc_aml

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_kyc_aml\`

## 🎯 Features to Test
- Risk rating workflow
- Review cycle computation
- Expiry flag
- Checklist fields

## 🧪 Workflow Scenario
- Create KYC file per partner.
- Complete document checklist and screening.
- Approve; next review computed from cycle.

## ⚠️ Watch Points
- Review overdue only flags approved files.
- Screening results recorded manually in v1.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_kyc_aml to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- risk rating workflow
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
