# sf_price_change_mgmt — Price Change Management

Plan, announce and apply price increases with product lines, delta % and effective dates.

## Quick Install

```bash
cp -r sf_price_change_mgmt /path/to/odoo/addons/
./odoo-bin -i sf_price_change_mgmt -d your_database
```

## Dependencies

`base, product, sale, mail`

## Workflow

- Build campaign (products, new prices, effective date).
- Announce.
- Apply at effective date (updates list prices).

## Features

- Campaigns — Reason, announcement date, effective date.
- Product Lines — Old price captured, new price, computed delta %.
- One-Click Apply — At effective date, apply updates product list prices.
- Date Gate — Cannot apply before the effective date.
- Cancel — Cancel any time before application.
- Multi-Company — Per-entity campaigns.
- Audit Trail — Chatter with application date.
- Role Groups — User and Manager.
- Standard Modules Only — base, product, sale, mail.

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
- **Price:** €199 (one-time)
