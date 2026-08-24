# HANDOFF TEST — sf_fx_hedging

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_fx_hedging\`

## 🎯 Features to Test
- Exposure scan groups open FX items correctly
- Coverage % computed per currency/direction
- Settlement gain/loss correct vs strike
- Multi-company isolation

## 🧪 Workflow Scenario
- Exposure Snapshots > Compute: net open FX per currency.
- Book forwards (direction, notional, strike, value date).
- Settle at maturity: spot-based gain/loss recorded.

## ⚠️ Watch Points
- Spot rate uses Odoo rate table - ensure rates exist for settlement dates.
- Coverage % matches hedges by direction (sell for receivable exposure).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, mail
Install: `Copy sf_fx_hedging to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- exposure scan groups open fx items correctly
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
