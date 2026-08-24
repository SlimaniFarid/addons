# sf_backorder_priority — Backorder Allocation & Priority

Allocate scarce stock to open backorders by configurable priority rules.

## Quick Install

```bash
cp -r sf_backorder_priority /path/to/odoo/addons/
./odoo-bin -i sf_backorder_priority -d your_database
```

## Dependencies

`base, sale, stock, mail`

## Workflow

- Create run (product, weights).
- Compute: score and allocate top-down.
- Apply reservations on winning deliveries.

## Features

- Priority Scoring — Score = days late + order value + customer priority, with adjustable weights.
- Shortage Detection — Open outgoing deliveries with unmet quantity for the product.
- Top-Down Allocation — Available stock allocated to highest scores first.
- Reserve — Apply reservations to the winning deliveries.
- Multi-Company — Per-entity runs.
- Currencies — Order value in company currency.
- Audit Trail — Chatter on runs.
- Role Groups — Allocation User and Manager.
- Standard Modules Only — base, sale, stock, mail.

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
