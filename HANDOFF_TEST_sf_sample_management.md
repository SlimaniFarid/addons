# HANDOFF TEST — sf_sample_management

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_sample_management\`

## 🎯 Features to Test
- Total cost = lines + shipping
- State flow enforced (ship after approve, etc.)
- Feedback gating before conversion
- Won/lost outcome tracking

## 🧪 Workflow Scenario
- Log request (customer, purpose, lines with costs).
- Approve -> record shipment reference.
- Feedback -> link sale order -> Converted (won) or Lost.

## ⚠️ Watch Points
- Shipping requires a shipment reference (tracking).
- Conversion requires a linked sale order.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, sale_management, stock, product, mail
Install: `Copy sf_sample_management to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- total cost = lines + shipping
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
