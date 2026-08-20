# Atelier & Maintenance Véhicules

Manage a vehicle fleet and its maintenance workshop: vehicles with
history, prioritized intervention requests, repair orders with
operations (hours) and parts, complete cost per order and per
vehicle, and cron alerts on urgent unassigned requests.

## Features

- Vehicle fleet with repair history
- Sequential numbering for vehicles, requests, orders, operations
  and parts
- Prioritized intervention requests (low/normal/high/urgent)
- Repair orders: draft → planned → in_progress → done → closed
- Operations and parts per order with status tracking
- Complete order cost: parts total + hours x hourly rate
- Per-vehicle cost report and printable repair order
- Cron alerts on urgent requests and overdue orders
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Atelier & Maintenance Véhicules**.

## Configuration

Assign the groups in Settings > Users:

- **Workshop User**: vehicles, requests, operations and parts.
- **Workshop Manager**: full access, assigning requests to orders
  and closing orders, all companies.

Company settings (Settings > Workshop):
- Default hourly rate.
- Number of days before an urgent request is alerted.

## Usage

1. Create vehicles and their owner.
2. Record intervention requests with priority.
3. The manager assigns a request to a repair order.
4. Mechanics record operations (hours) and parts.
5. The order cost and the vehicle cost report are computed.

## Permissions

- `sf_vehicle_workshop.group_sf_workshop_user` — read/write limited.
- `sf_vehicle_workshop.group_sf_workshop_manager` — full access,
  assigning requests and closing orders.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).