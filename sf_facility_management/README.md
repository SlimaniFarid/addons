# sf_facility_management — Facility & Space Management

Sites, rooms and bookings with capacity control and conflict detection.

## Quick Install

```bash
cp -r sf_facility_management /path/to/odoo/addons/
./odoo-bin -i sf_facility_management -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Register sites and rooms.
- Book rooms (conflict-checked).
- Manage via calendar view.

## Features

- Sites — Address, surface, owned/leased with lease reference.
- Rooms — Type, capacity, floor, surface per site.
- Bookings — Datetime ranges with purpose and attendees.
- Conflict Detection — Double-bookings blocked at save.
- Calendar View — Bookings on a calendar.
- Multi-Company — Per-entity sites.
- Audit Trail — Chatter on sites and bookings.
- Role Groups — Facility User and Manager.
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
