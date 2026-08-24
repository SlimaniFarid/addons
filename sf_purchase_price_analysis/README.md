# sf_purchase_price_analysis — Purchase Price Variance Analysis

PPV per product/vendor vs standard cost from posted bills, variance flags and vendor comparison.

## Quick Install

```bash
cp -r sf_purchase_price_analysis /path/to/odoo/addons/
./odoo-bin -i sf_purchase_price_analysis -d your_database
```

## Dependencies (auto-installed)

`base, account, purchase, product, mail`

## Workflow

- New analysis: period, optional vendor, tolerance %.
- Compute -> lines per product/vendor.
- Review alerts, act on outliers.

## Features

- PPV Runs — Actual average purchase price per product/vendor from posted bills in the period.
- Vs Standard Cost — Variance amount and % against product standard price.
- Tolerance Alerts — Lines beyond your tolerance % flagged in red.
- Vendor Comparison — Same product, different vendors: spot who is expensive.
- Pivot Ready — Analyze variance by product, vendor or category.
- Multi-Currency — Company currency amounts.
- Multi-Company — Per-entity analyses.
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
- **Price:** €249 (one-time)
