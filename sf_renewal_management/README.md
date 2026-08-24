# sf_renewal_management — Customer Contract Renewals

Renewal pipeline with notice deadlines, auto-renew flags, churn risk and renewal outcomes.

## Quick Install

```bash
cp -r sf_renewal_management /path/to/odoo/addons/
./odoo-bin -i sf_renewal_management -d your_database
```

## Dependencies

`base, sale, mail`

## Workflow

- Log contracts (customer, type, term, notice period, value).
- Track notice/expiry countdowns.
- Flag expiring, renew or mark lost.

## Features

- Notice Deadlines — Notice deadline and days-to-notice computed automatically from the notice period.
- Auto-Renew Flags — Mark contracts with auto-renewal clauses and renew in one click with new end date.
- Expiring Pipeline — Kanban by state: active, expiring, renewed, lost, expired.
- Churn Risk — Rate each contract low/medium/high risk with next action follow-up.
- Contract Value — Annual value and proposed renewal value per contract.
- Account Owners — Assign each contract to the responsible account manager.
- Multi-Company — Per-entity contracts with record rules.
- Audit Trail — Chatter on every state change.
- Standard Modules Only — base, sale, mail.

## Compatibility

| Odoo Version | Status |
|--------------|--------|
| 18.0 | Primary target |
| 19.0 | Compatible |
| Editions | Community & Enterprise |
| Hosting | Odoo.sh, on-premise, Docker |

## License & Support

- **License:** OPL-1 — one-time purchase, lifetime usage
- **Support:** tech5262@gmail.com
- **Author:** Ethan Miller
- **Price:** €249 (one-time)
