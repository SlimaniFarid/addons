# HANDOFF TEST — sf_product_eol

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_product_eol\`

## 🎯 Features to Test
- Stock/order computation
- Phase-out state flow
- Sale blocking
- Cancel path

## 🧪 Workflow Scenario
- Announce EOL (dates, replacement).
- Phase out; monitor stock/orders.
- Discontinue (blocked while open orders).

## ⚠️ Watch Points
- Discontinue sets product sale_ok=False.
- Open orders block discontinuation by design.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, product, sale, stock, mail
Install: `Copy sf_product_eol to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- stock/order computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
