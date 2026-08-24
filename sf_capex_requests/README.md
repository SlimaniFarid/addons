# sf_capex_requests — CAPEX Request & Approval

Capital expenditure requests with multi-level approvals, payback/ROI fields and capitalization tracking.

## Quick Install

```bash
cp -r sf_capex_requests /path/to/odoo/addons/
./odoo-bin -i sf_capex_requests -d your_database
```

## Dependencies (auto-installed)

`base, mail`

## Workflow

- Create request with business case and approval chain.
- Submit -> approve level by level.
- Mark Ordered (PO ref) -> Capitalized (asset ref).

## Features

- Structured Requests — Category, department, business case, requested vs approved amount, expected date.
- Multi-Level Approvals — Approval chain with per-level approver, comment and date; auto-advance when all approved.
- Payback & Benefit — Annual benefit and computed payback years on every request.
- Order & Capitalize — Mark Ordered with PO reference, then Capitalized with asset reference.
- Kanban Pipeline — Requests grouped by state for instant portfolio view.
- Multi-Company — Per-entity requests with isolation.
- Audit Trail — Chatter: submissions, approvals, rejections with dates.
- Role Groups — Requester and Manager groups.
- Standard Modules Only — base, mail. No extra dependencies.

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
