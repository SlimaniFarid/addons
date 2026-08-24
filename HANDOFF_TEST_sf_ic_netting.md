# HANDOFF TEST — sf_ic_netting

## 📍 Location
`C:\Users\USER\Documents\Default Project\addons\sf_ic_netting\`

## 🎯 Features to Test
- Compute produces correct nets on sample IC invoices
- Settlement entries posted and balanced
- Dispute flagging and resolution works
- Multi-company isolation

## 🧪 Workflow Scenario
- Create session: period + participating entities.
- Compute Positions -> net per company pair.
- Confirm, resolve disputes, Settle (posts net entries).

## ⚠️ Watch Points
- Partner-company matching uses res.company.partner_id - ensure company partner records exist.
- Settlement posts in the payer entity; mirror entries follow your IC process.
- Due-to/due-from accounts fall back to first receivable/payable account - set system params sf_ic_netting.due_from/to_account_id_<company> for precision.

## 🔧 Instance
Odoo 18/19 (Community/Enterprise). Deps: base, account, mail
Install: `Copy sf_ic_netting to addons, restart, install from Apps.`

## ✅ Acceptance
- Installs clean on Odoo 18.0/19.0
- compute produces correct nets on sample ic invoices
- No tracebacks on the full workflow
- Security groups enforce permissions

## 📞 Contact
tech5262@gmail.com — handoff 2026-08-24 (cycles 4-13 batch)

> Static QC + offline validation only. Functional testing on live Odoo pending (test agent).
