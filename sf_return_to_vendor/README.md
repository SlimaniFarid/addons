# sf_return_to_vendor — Return to Vendor (RTV)

Defective and excess goods returns to suppliers: dispositions (return/credit/replace/scrap), return pickings and debit note tracking.

## Quick Install

```bash
cp -r sf_return_to_vendor /path/to/odoo/addons/
./odoo-bin -i sf_return_to_vendor -d your_database
```

## Dependencies (auto-installed)

`base, stock, purchase, account, mail`

## Workflow

- Create RTV: vendor, reason, lines (lot, cost, disposition).
- Confirm -> Create Return Picking (return/repair lines).
- Ship, then Settle with debit note reference.

## Features

- RTV Orders — Vendor, origin receipt, reason (defective, wrong item, overstock, recall, warranty).
- Dispositions per Line — Return for credit, return for repair, vendor replacement, scrap on site.
- One-Click Return Picking — Outgoing picking to the vendor with lots preserved.
- Value Tracked — Unit cost, line and total RTV value.
- Debit Notes — Debit note reference required before settlement.
- Multi-Company — Per-entity orders and lines.
- Audit Trail — Chatter with state changes and authorizations.
- Role Groups — RTV User and Manager.
- Standard Modules Only — base, stock, purchase, account, mail.

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
