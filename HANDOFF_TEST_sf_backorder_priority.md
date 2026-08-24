# HANDOFF TEST — sf_backorder_priority

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_backorder_priority\`

## 🎯 Features to Test
- Shortage detection
- Ranked allocation within available
- Apply assigns pickings
- Weights affect ranking

## 🧪 Workflow Scenario
- Create run (product, weights).
- Compute: score and allocate top-down.
- Apply reservations on winning deliveries.

## ⚠️ Watch Points
- Score = lateness + value/1000 + customer weight.
- One product per run.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, sale, stock, mail
Install: `Copy sf_backorder_priority to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- shortage detection
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
