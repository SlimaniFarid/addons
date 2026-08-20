# SF Restaurant

Restaurant, Cafe & In-Room Dining management module for Odoo 18.

## Features

- Dining room tables with states and zones.
- Reservations with capacity control to avoid overbooking.
- Menu categories and items with per-service availability.
- Table orders with kitchen ticket transmission.
- Daily revenue tracking by service and by table.
- Activity TODOs for kitchen tickets and end-of-service actions.
- Cron alerts for upcoming reservations.
- Multi-company support with record rules per company.
- QWeb reports: Kitchen Ticket, Table Bill and Daily Revenue.

## Configuration

In Settings > Restaurant you can configure:

- The default restaurant layout (zones and tables).
- Number of days before a reservation used by the reminder cron (default 1).

## Usage

1. Create zones and tables.
2. Create menu categories and items.
3. Take reservations against tables.
4. Open table orders and send kitchen tickets.
5. Close orders and track daily revenue by service.

## Permissions

- `sf_restaurant.group_sf_restaurant_user` - read/write limited.
- `sf_restaurant.group_sf_restaurant_manager` - full access and configuration.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.