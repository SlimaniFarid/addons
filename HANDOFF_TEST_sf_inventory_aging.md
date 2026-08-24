# HANDOFF TEST — sf_inventory_aging

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_inventory_aging\`

## 🎯 Features to Test
- Aging days correct
- Bucket assignment
- Provision = value x %
- Dead stock count

## 🧪 Workflow Scenario
- Create run (as-of, warehouse, bucket %).
- Compute from quants and last moves.
- Review buckets and provisions.

## ⚠️ Watch Points
- Last movement = last done move line in internal location.
- No movement found = as_of date used.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, stock, product, mail
Install: `Copy sf_inventory_aging to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- aging days correct
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
