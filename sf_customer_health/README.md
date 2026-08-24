# sf_customer_health — Customer Health & Churn Risk

Post-sale health scoring: revenue recency, trend and overdue signals with churn risk rating.

## Quick Install

```bash
cp -r sf_customer_health /path/to/odoo/addons/
./odoo-bin -i sf_customer_health -d your_database
```

## Dependencies

`base, sale, account, mail`

## Workflow

- Register key accounts.
- Refresh signals (revenue, recency, overdue).
- Work at-risk customers first.

## Features

- Health Score 0-100 — Weighted signals: order recency (40), revenue trend (35), overdue (25).
- Revenue Trend — Last 12 months vs previous 12 months with delta %.
- Recency — Days since last confirmed sale order.
- Overdue Signal — Open receivable exposure detected.
- Risk Ratings — Healthy, watch, at-risk, churn - auto-computed.
- Next Actions — Action date and note per customer.
- Multi-Company — Per-entity health.
- Audit Trail — Chatter with refresh history.
- Standard Modules Only — base, sale, account, mail.

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
