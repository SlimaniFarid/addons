# HANDOFF TEST — sf_load_planning

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_load_planning\`

## 🎯 Features to Test
- Totals computed from assigned pickings
- Overload flags and Plan blocking
- Lifecycle transitions enforced
- Multi-company isolation

## 🧪 Workflow Scenario
- Create load: carrier, vehicle, departure, capacities.
- Assign deliveries + route stops.
- Plan (capacity validated) -> Loaded -> Departed -> Complete.

## ⚠️ Watch Points
- Weights/volumes from product fields x quantities.
- A picking belongs to a single load.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, stock, mail
Install: `Copy sf_load_planning to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- totals computed from assigned pickings
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
