# sf_change_requests — Change Request & CAB Workflow

IT and operational changes with CAB review, risk levels, rollback plans and closure.

## Quick Install

```bash
cp -r sf_change_requests /path/to/odoo/addons/
./odoo-bin -i sf_change_requests -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Submit (rollback plan mandatory).
- CAB review with votes; close CAB decides.
- Implement, review, close or fail.

## Features

- Change Requests — Type, description, impact analysis, implementation plan.
- Rollback Mandatory — Cannot submit without a rollback plan.
- CAB Review — Member votes with comments; approval % computed.
- Risk Levels — Low/medium/high with color coding.
- Lifecycle — Submitted, CAB, approved, implemented, closed - or failed.
- PIR — Post-implementation review on closure.
- Multi-Company — Per-entity changes.
- Audit Trail — Chatter with all decisions.
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
- **Price:** €249 (one-time)
