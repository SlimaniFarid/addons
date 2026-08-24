# sf_bank_stmt_import_pro — Bank Statement Import Pro (MT940 / CAMT / CSV)

Import any bank statement into Odoo Accounting: MT940, CAMT.053, OFX, QIF
or any bank CSV — per-bank templates, duplicate detection, multi-currency.

## Quick Install

```bash
cp -r sf_bank_stmt_import_pro /path/to/odoo/addons/
# Settings -> Update Apps List -> Install
./odoo-bin -i sf_bank_stmt_import_pro -d your_database
```

## Dependencies (auto-installed)

| Module | Purpose |
|--------|---------|
| `base` | Core, sequences, partners, currencies |
| `account` | Bank journals, statements, statement lines |
| `mail` | Chatter, activities |

## Post-Install Configuration

### 1. User Groups

| Group | Permissions |
|-------|-------------|
| **Bank Import User** | Create runs, parse, import |
| **Bank Import Manager** | Full CRUD incl. delete templates/runs |

### 2. Templates (Bank Import Pro > Templates)

Required only for **CSV** files. MT940/CAMT.053/OFX/QIF parse directly.

| Field | Example |
|-------|---------|
| Date Column (0-based) | 0 |
| Amount Column | 1 |
| Debit/Credit Column | 2 (with Debit Marker `D`) |
| Reference / Partner / Communication Columns | 3 / 4 / 5 |
| Delimiter / Encoding | `;` / UTF-8 with BOM |
| Date Format | 23/08/2026 |
| Decimal / Thousands Separator | `,` / `.` |

### 3. Liability of Balances

MT940 (`:60F:`/`:62F:`) and CAMT.053 (`Bal` OPBD/CLBD) opening/closing
balances are written to the created statement automatically.

## Workflow

```
1. Bank Import Pro > Import Runs > New
2. Pick bank journal + template (or MT940/CAMT/OFX/QIF template)
3. Upload file -> "Parse File"
4. Review preview grid (duplicates red, stats at top)
5. "Import Lines" -> bank statement created, ready to reconcile
```

## Duplicate Detection

- Hash = SHA-256 of `journal_id | date | amount | reference[:80]`
- Compared against:
  - Existing `account.bank.statement.line` of the same journal (last 5000)
  - Lines parsed in the current batch
- Flagged duplicates are skipped on import (uncheck "Skip Duplicates"
  to force)

## Multi-Currency

If a parsed line carries an ISO currency code different from the journal
currency and that currency exists (active) in Odoo, the statement line is
created with `foreign_currency_id` so amounts and rates stay correct.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Parsing failed: No :61: lines" | File is not MT940 — check template format |
| "No data rows could be parsed from CSV" | Verify column indices and date format in the template |
| All lines flagged duplicate | Period already imported — this is the dedup working; force-import only if intentional |
| Partner not matched | Matching is exact-name; match manually at reconciliation |

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
- **Price:** €299 (one-time)
