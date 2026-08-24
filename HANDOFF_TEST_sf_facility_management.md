# HANDOFF TEST — sf_facility_management

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_facility_management\`

## 🎯 Features to Test
- Conflict constraint works
- Time validation
- Room types
- Calendar view

## 🧪 Workflow Scenario
- Register sites and rooms.
- Book rooms (conflict-checked).
- Manage via calendar view.

## ⚠️ Watch Points
- Overlap bookings blocked by constraint.
- Cancelled bookings do not conflict.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, mail
Install: `Copy sf_facility_management to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- conflict constraint works
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 14-33 batch)

> Static QC only. Functional testing on live Odoo pending (test agent).
