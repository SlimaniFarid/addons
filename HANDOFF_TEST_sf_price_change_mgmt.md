# HANDOFF TEST — sf_price_change_mgmt

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_price_change_mgmt\`

## 🎯 Features to Test
- Delta % computation
- Date gating
- Price application
- Cancel before apply

## 🧪 Workflow Scenario
- Build campaign (products, new prices, effective date).
- Announce.
- Apply at effective date (updates list prices).

## ⚠️ Watch Points
- Apply blocked before effective date.
- Old price captured at apply time.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, product, sale, mail
Install: `Copy sf_price_change_mgmt to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- delta % computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
