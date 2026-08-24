# HANDOFF TEST — sf_data_dedup

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_data_dedup\`

## 🎯 Features to Test
- 4 strategies produce correct groups
- Group states
- Rescan clean
- Company scope

## 🧪 Workflow Scenario
- Create scan (strategy).
- Run scan: duplicate groups appear.
- Review, merge natively, mark merged.

## ⚠️ Watch Points
- Detection only; merge uses native tool.
- Strategies: exact name, name+city, VAT, email.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_data_dedup to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- 4 strategies produce correct groups
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
