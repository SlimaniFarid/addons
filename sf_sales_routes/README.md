# Field Sales Routes & Territory Management

Plan and track field sales activities: territories, routes and
visits with check-in/check-out, orders, opportunities and objectives.

## Features

- Territory management with customer assignment
- Route planning with ordered visits
- Visit check-in / check-out with timestamps
- Visit results (order, opportunity, information)
- Order and opportunity creation from a visit
- Objectives per territory and period
- Calendar and kanban boards for field sales
- Automatic marking of missed visits (daily cron)

## Installation

Copy the module to your addons path, update the app list and
install **Field Sales Routes & Territory Management**.

## Configuration

Assign the groups in Settings > Users:

- **Sales Routes User**: view territories, manage tours and visits.
- **Sales Routes Manager**: full access (territories, objectives,
  tours, visits).

## Usage

1. Create territories and assign a salesperson per territory.
2. Create a tour for a date, add ordered visits with planned times.
3. During the tour: check-in and check-out each visit.
4. Create a sale order or opportunity directly from a completed visit.
5. Track progress and objectives in the menus and dashboard.

## Permissions

- `sf_sales_routes.group_route_user` — read/write limited.
- `sf_sales_routes.group_route_manager` — full access.
- Record rules restrict users to their own tours or company.

## Dependencies

- base
- sales
- crm

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).