# Yard Management

Live trailer tracking, gate check-in/out, dock assignment, jockey shunt
moves and detention/demurrage billing — all inside Odoo.

## Features
- Yard map with zones and numbered locations (dock, parking, waiting, maintenance, customs)
- Trailer inventory with status, carrier, dwell clock and linked pickings
- Gate check-in / check-out (manual or QR-ready)
- Dock door assignment with occupancy guards
- Directed jockey shunt moves with timing trail
- Detention engine: free time per carrier, warning at 80%, chargeable beyond
- Monthly grouped vendor invoices for detention charges
- KPIs: occupancy by zone, average dwell, detention cost per day
- Multi-company with record rules

## Installation
Copy to addons path, update apps list, install **Yard Management**.

## Configuration
1. Settings > Users: assign *Yard Management / User* or / Manager.
2. Create zones and locations under **Yard Management > Zones & Locations**.
3. Set carrier free time + rate on the partner form.

## Permissions
- `sf_yard_management.group_sf_yard_user`
- `sf_yard_management.group_sf_yard_manager`

## Dependencies
base, mail, account, stock

## Compatibility
Odoo 18.0 and Odoo 19.0.
