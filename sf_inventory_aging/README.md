# sf_inventory_aging — Inventory Aging & Obsolescence

Stock aging buckets from last movement, slow-mover detection and obsolescence provision suggestions.

## Quick Install

```bash
cp -r sf_inventory_aging /path/to/odoo/addons/
./odoo-bin -i sf_inventory_aging -d your_database
```

## Dependencies

`base, stock, product, mail`

## Workflow

- Create run (as-of, warehouse, bucket %).
- Compute from quants and last moves.
- Review buckets and provisions.

## Features

- Aging per Product/Lot — Days since last stock movement computed per quant.
- 4 Buckets — 0-30, 31-90, 91-180 and 180+ days with configurable provision %.
- Slow Movers — Flag stock sitting beyond 180 days as dead stock.
- Provision Suggestions — Provision amount = stock value x bucket %, ready for your accountants.
- Per Warehouse — Filter the run by warehouse.
- Multi-Company — Per-entity analyses.
- Currencies — Valuation at standard cost.
- Audit Trail — Chatter on runs.
- Standard Modules Only — base, stock, product, mail.

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
