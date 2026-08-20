# Hotel PMS

Rooms and types with rates, multi-night reservations without
overbooking, check-in / check-out, additional charged services,
housekeeping and computed night billing, with daily cron alerts on
departures and housekeeping.

## Features

- Room fleet with statuses (available / occupied / maintenance /
  reserved)
- Sequential numbering for rooms, reservations, extras and
  housekeeping
- Multi-night reservations with anti-overbooking control
- Check-in / check-out workflow reserved to managers
- Additional charged services (extras)
- Computed nights and stay total
- Housekeeping planning and follow-up
- Daily departure and housekeeping alerts via cron (deduplicated)
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Hotel PMS**.

## Configuration

Assign the groups in Settings > Users:

- **Hotel User**: rooms, reservations and housekeeping.
- **Hotel Manager**: full access, check-in / check-out, charging
  extras and closing housekeeping, all companies.

Company settings (Settings > Hotel):
- Number of days for the departure alert window.

## Usage

1. Create rooms with type, capacity and base price.
2. Record a reservation (availability is checked).
3. Check the guest in; the room becomes occupied.
4. Charge additional services during the stay.
5. Check the guest out; the night billing is computed.

## Permissions

- `sf_hotel_pms.group_sf_hotel_user` — read/write limited.
- `sf_hotel_pms.group_sf_hotel_manager` — full access, check-in /
  check-out, charging extras and closing housekeeping.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).