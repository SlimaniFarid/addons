# HANDOFF TEST — sf_purchase_price_analysis

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_purchase_price_analysis\`

## 🎯 Features to Test
- Actual avg price matches manual computation
- Variance amount/% correct
- Alerts flagged beyond tolerance
- Recompute replaces lines

## 🧪 Workflow Scenario
- New analysis: period, optional vendor, tolerance %.
- Compute -> lines per product/vendor.
- Review alerts, act on outliers.

## ⚠️ Watch Points
- Baseline = product standard_price; zero standard => 0% variance.
- v1 analyzes invoices only (credit notes roadmap).

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, purchase, product, mail
Install: `Copy sf_purchase_price_analysis to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- actual avg price matches manual computation
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
