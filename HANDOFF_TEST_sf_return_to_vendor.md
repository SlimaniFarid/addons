# HANDOFF TEST — sf_return_to_vendor

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_return_to_vendor\`

## 🎯 Features to Test
- RTV value = sum(line qty x unit cost)
- Return picking created with correct moves/lots
- Settlement requires debit note ref
- Cancel blocked once picking done

## 🧪 Workflow Scenario
- Create RTV: vendor, reason, lines (lot, cost, disposition).
- Confirm -> Create Return Picking (return/repair lines).
- Ship, then Settle with debit note reference.

## ⚠️ Watch Points
- Return picking uses outgoing type + customer location as vendor destination (simplified v1).
- Scrap/replace dispositions excluded from the picking.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, stock, purchase, account, mail
Install: `Copy sf_return_to_vendor to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- rtv value = sum(line qty x unit cost)
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
