# sf_credit_insurance — Credit Insurance & Insured Exposure

Insurer policies, approved buyer limits with coverage % and bad-debt claims with indemnity tracking.

## Quick Install

```bash
cp -r sf_credit_insurance /path/to/odoo/addons/
./odoo-bin -i sf_credit_insurance -d your_database
```

## Dependencies

`base, account, mail`

## Workflow

- Record policy (insurer, coverage, period).
- Request buyer limits; record decisions.
- File claims; indemnity computed; track settlement.

## Features

- Insurance Policies — Insurer, policy number, coverage %, premium and period.
- Insured Buyer Limits — Requested vs approved limits with insurer decision workflow.
- Claims — Overdue amount, claimed amount, indemnity computed from coverage.
- Waiting Period — Configurable waiting period per claim.
- Settlement States — Submitted, accepted, partially paid, paid, rejected.
- Multi-Company — Per-entity policies.
- Currencies — Company currency amounts.
- Audit Trail — Chatter on policies, buyers and claims.
- Standard Modules Only — base, account, mail.

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
