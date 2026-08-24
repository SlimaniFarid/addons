# sf_data_dedup — Duplicate Records Audit & Merge

Detect duplicate partners with 4 strategies, review groups and track merges.

## Quick Install

```bash
cp -r sf_data_dedup /path/to/odoo/addons/
./odoo-bin -i sf_data_dedup -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Create scan (strategy).
- Run scan: duplicate groups appear.
- Review, merge natively, mark merged.

## Features

- 4 Scan Strategies — Exact name, name + city, same VAT, same email.
- Duplicate Groups — Members listed per group with match key.
- Review Workflow — Open, merged (via native merge), ignored, reopen.
- Company Scope — Scans respect company isolation.
- Audit Trail — Chatter on scans.
- Role Groups — Data Steward and Manager.
- Standard Modules Only — base, mail.
- Master Data Hygiene — Better mailings, fewer double invoices.
- Mobile Friendly — Review groups anywhere.

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
- **Price:** €179 (one-time)
