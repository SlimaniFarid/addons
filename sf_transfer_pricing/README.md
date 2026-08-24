# sf_transfer_pricing — Transfer Pricing Engine

OECD-compliant intercompany pricing (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation.

## Quick Install

```bash
cp -r sf_transfer_pricing /path/to/odoo/addons/
./odoo-bin -i sf_transfer_pricing -d your_database
```

## Dependencies (auto-installed)

`base, account, mail`

## Workflow

- Create a policy per entity pair (method, markup, validity).
- Review flagged transactions in Transaction Analysis.
- Maintain Master/Local File documentation per fiscal year.

## Features

- 4 OECD Methods — CUP, Cost-Plus, Resale-Minus and TNMM with markup %, target margin and benchmarking notes per policy.
- Policies per Company Pair — Selling entity, buying entity and IC partner with validity dates and APA references.
- Transaction Analysis — Actual vs computed arm-length price with variance amount and % per intercompany line.
- Review Thresholds — Transactions beyond tolerance flagged for documented review with reviewer sign-off.
- Master File / Local File — Documentation register per fiscal year with sections, owner, review date and status workflow.
- Multi-Company Native — Policies and analysis scoped per entity with record rules.
- CbCR-Ready — Documentation structure aligned with BEPS Action 13 expectations.
- Audit Trail — Chatter on policies, transactions and documentation: who reviewed what and when.
- Standard Modules Only — base, account, mail. No third-party libraries.

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
- **Price:** €399 (one-time)
