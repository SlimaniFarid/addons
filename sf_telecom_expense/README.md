# sf_telecom_expense — Telecom Expense Management

Mobile/data/landline lines per employee with plan costs and monthly invoice variance audit.

## Quick Install

```bash
cp -r sf_telecom_expense /path/to/odoo/addons/
./odoo-bin -i sf_telecom_expense -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Register lines (employee, provider, plan cost).
- Audit invoices: expected vs invoiced.
- Investigate variances beyond tolerance.

## Features

- Lines Registry — Employee, department, provider, number, type, monthly cost.
- Contract End Tracking — Ending-soon flags at 30 days.
- Invoice Audits — Expected cost from active lines vs invoiced amount.
- Variance Alerts — Beyond tolerance % flagged red.
- Multi-Company — Per-entity lines and audits.
- Currencies — Company currency.
- Audit Trail — Chatter on lines and audits.
- Role Groups — User and Manager.
- Standard Modules Only — base, mail.

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
- **Price:** €229 (one-time)
