# HANDOFF TEST — sf_supplier_rebates

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_supplier_rebates\`

## 🎯 Features to Test
- Accrual math correct per deal type (%, per unit, bonus)
- Category scoping filters bill lines
- Threshold progress on turnover bonus deals
- Claim -> settled flow updates deal state

## 🧪 Workflow Scenario
- Record deal (type, period, threshold/rate, category).
- Activate -> Compute Accruals monthly.
- Create claim, submit, mark credit received.

## ⚠️ Watch Points
- Accruals are computed amounts; ledger posting stays in your process (v1.1).
- Recomputing deletes unclaimed accruals and rebuilds.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, purchase, product, mail
Install: `Copy sf_supplier_rebates to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- accrual math correct per deal type (%, per unit, bonus)
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
