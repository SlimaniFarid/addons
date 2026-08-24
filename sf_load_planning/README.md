# sf_load_planning — Load & Pallet Planning

Build truck loads from pickings with capacity checks (weight, volume, pallets), route stops and lifecycle.

## Quick Install

```bash
cp -r sf_load_planning /path/to/odoo/addons/
./odoo-bin -i sf_load_planning -d your_database
```

## Dependencies (auto-installed)

`base, stock, mail`

## Workflow

- Create load: carrier, vehicle, departure, capacities.
- Assign deliveries + route stops.
- Plan (capacity validated) -> Loaded -> Departed -> Complete.

## Features

- Load Plans — Carrier, vehicle ref, warehouse, departure date.
- Assign Deliveries — Pickings assigned to loads with route stop per delivery.
- Capacity Checks — Max weight, volume and pallets with overload flags; planning blocked on overload.
- Route Stops — Sequenced stops with planned arrival times.
- Lifecycle — Draft, Planned, Loaded, Departed, Completed.
- Multi-Company — Per-entity loads.
- Audit Trail — Chatter on every state change.
- Role Groups — Load Planning User and Manager.
- Standard Modules Only — base, stock, mail.

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
