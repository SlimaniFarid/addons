# sf_policy_waivers — Policy Exception & Waiver Management

Time-boxed policy waivers with risk assessment, compensating controls and approval workflow.

## Quick Install

```bash
cp -r sf_policy_waivers /path/to/odoo/addons/
./odoo-bin -i sf_policy_waivers -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Request waiver (policy, reason, risk, controls, window).
- Approve or reject with reason.
- Track expiry flag.

## Features

- Waiver Requests — Policy waived, justification, department.
- Risk Assessment — Risk level plus written assessment.
- Compensating Controls — Mandatory controls description.
- Validity Window — From/to dates - exceptions are temporary.
- Auto-Expiry Flag — Expired waivers flagged automatically.
- Approval Workflow — Approve or reject with reason and approver.
- Multi-Company — Per-entity waivers.
- Audit Trail — Chatter with decisions.
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
- **Price:** €179 (one-time)
