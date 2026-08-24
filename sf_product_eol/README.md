# sf_product_eol — Product End-of-Life & Last-Time-Buy

Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping and sale blocking.

## Quick Install

```bash
cp -r sf_product_eol /path/to/odoo/addons/
./odoo-bin -i sf_product_eol -d your_database
```

## Dependencies

`base, product, sale, stock, mail`

## Workflow

- Announce EOL (dates, replacement).
- Phase out; monitor stock/orders.
- Discontinue (blocked while open orders).

## Features

- EOL Records — Announcement, EOL and last-time-buy dates per product.
- Replacement Mapping — Point customers to the successor product.
- Stock Visibility — Remaining internal stock computed.
- Open Order Checks — Open sale orders and lines detected before discontinuation.
- Sale Blocking — Discontinue blocks sales on the product.
- Communication Plan — Rich-text customer communication plan.
- Multi-Company — Per-entity records.
- Audit Trail — Chatter with state changes.
- Standard Modules Only — base, product, sale, stock, mail.

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
