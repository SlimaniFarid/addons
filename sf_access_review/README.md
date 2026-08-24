# sf_access_review — Access Recertification

Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions.

## Quick Install

```bash
cp -r sf_access_review /path/to/odoo/addons/
./odoo-bin -i sf_access_review -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Create campaign (scope, due date).
- Generate review lines per user.
- Keep/revoke each, close when all decided.

## Features

- Campaigns — All users or admin/privileged only, with due date.
- Auto-Generated Reviews — One line per user with current groups summary.
- Keep / Revoke — Reviewer decisions with dates and comments.
- Close Gate — Campaign closes only when every review is decided.
- Evidence — Complete decision trail for auditors.
- Multi-Company — Per-entity campaigns.
- Audit Trail — Chatter on campaigns.
- Role Groups — Reviewer and Manager.
- Standard Modules Only — base, mail.

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
- **Price:** €229 (one-time)
