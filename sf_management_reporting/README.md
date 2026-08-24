# sf_management_reporting — Monthly Management Report Pack

Board-ready monthly pack: revenue, costs, margin KPIs vs previous month with commentary.

## Quick Install

```bash
cp -r sf_management_reporting /path/to/odoo/addons/
./odoo-bin -i sf_management_reporting -d your_database
```

## Dependencies

`base, account, sale, purchase, mail`

## Workflow

- Create report (month period).
- Compute KPIs from posted entries.
- Add KPI lines and commentary, finalize.

## Features

- Revenue — Posted customer invoices untaxed total for the month.
- Vendor Costs — Posted vendor bills untaxed total.
- Gross Margin — Margin and margin % computed automatically.
- Trend — Revenue vs previous month with delta %.
- KPI Lines — Custom KPIs with previous values and delta %.
- Commentary — Executive commentary per report.
- Finalize — Freeze the pack once final.
- Multi-Company — Per-entity packs.
- Standard Modules Only — base, account, sale, purchase, mail.

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
