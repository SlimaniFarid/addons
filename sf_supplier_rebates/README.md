# sf_supplier_rebates — Supplier Rebates & Retro-discounts

Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking.

## Quick Install

```bash
cp -r sf_supplier_rebates /path/to/odoo/addons/
./odoo-bin -i sf_supplier_rebates -d your_database
```

## Dependencies (auto-installed)

`base, account, purchase, product, mail`

## Workflow

- Record deal (type, period, threshold/rate, category).
- Activate -> Compute Accruals monthly.
- Create claim, submit, mark credit received.

## Features

- Deal Types — Turnover bonus above threshold, retro % on purchases, or fixed rebate per unit.
- Category Scope — Scope deals to a product category or the full vendor portfolio.
- Auto Accrual — Monthly accrual computed from posted vendor bills in the deal period.
- Threshold Progress — Live progress toward volume thresholds.
- Claims — Claim to vendor with amount, credit note reference and settlement states.
- Multi-Company — Per-entity deals.
- Currencies — Company currency amounts.
- Audit Trail — Chatter on deals and claims.
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
- **Price:** €279 (one-time)
