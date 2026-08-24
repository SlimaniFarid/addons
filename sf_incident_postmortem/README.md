# sf_incident_postmortem — Incident Post-Mortem & Lessons Learned

Operational incident reviews: severity, timeline, root cause, corrective actions and lessons library.

## Quick Install

```bash
cp -r sf_incident_postmortem /path/to/odoo/addons/
./odoo-bin -i sf_incident_postmortem -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Log incident (severity, category, detection time).
- Analyze impact/root cause.
- Add actions, capture lessons, close.

## Features

- Severity S1-S4 — Critical to low with color-coded lists.
- Timeline — Detection and resolution timestamps, computed duration.
- Root Cause — Structured RCA section per incident.
- Actions — Corrective and preventive actions with owners and due dates.
- Lessons Learned — Captured per incident, searchable across the library.
- Categories — IT, production, logistics, quality, safety, supplier.
- Multi-Company — Per-entity incidents.
- Audit Trail — Chatter on every incident.
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
- **Price:** €199 (one-time)
