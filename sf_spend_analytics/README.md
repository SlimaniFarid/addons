# sf_spend_analytics — Procurement Spend Analytics

Spend per vendor and category from posted bills, PO coverage and maverick buying detection.

## Quick Install

```bash
cp -r sf_spend_analytics /path/to/odoo/addons/
./odoo-bin -i sf_spend_analytics -d your_database
```

## Dependencies

`base, account, purchase, product, mail`

## Workflow

- Create run (period, tolerance).
- Compute from posted bills.
- Review maverick vendors beyond tolerance.

## Features

- Analysis Runs — Spend per vendor computed from posted vendor bills in the period.
- Category View — Main product category per vendor line.
- PO Coverage — Amount linked to purchase orders vs off-contract spend.
- Maverick Detection — Bills without PO flagged beyond your tolerance %.
- Totals — Total spend and total maverick per run.
- Multi-Company — Per-entity analyses.
- Currencies — Company currency amounts.
- Audit Trail — Chatter on runs.
- Standard Modules Only — base, account, purchase, product, mail.

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
- **Price:** €299 (one-time)
