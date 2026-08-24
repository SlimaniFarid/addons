# sf_customer_rebates — Customer Rebates & Turnover Bonuses

Sell-side rebate deals with accrual from invoices and credit note settlement.

## Quick Install

```bash
cp -r sf_customer_rebates /path/to/odoo/addons/
./odoo-bin -i sf_customer_rebates -d your_database
```

## Dependencies

`base, account, sale, product, mail`

## Workflow

- Record deal (customer, period, type).
- Activate, compute accruals monthly.
- Settle with credit note reference.

## Features

- Deal Types — Retro % on sales, turnover bonus above threshold, fixed per unit.
- Category Scope — Scope to a product category or the full portfolio.
- Auto Accrual — Monthly accrual computed from posted customer invoices.
- Sales Progress — Total sales in period per deal.
- Settlement — Credit note reference and settled date.
- Multi-Company — Per-entity deals.
- Currencies — Company currency amounts.
- Audit Trail — Chatter on deals.
- Standard Modules Only — base, account, sale, product, mail.

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
