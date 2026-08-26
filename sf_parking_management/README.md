# SF Parking Management

Parking Lot &amp; Garage Management module for Odoo 18.

## Features

- Parking sites with capacity, hourly and daily rates.
- Zones and places with free / occupied / reserved / out-of-service states.
- Entry and exit tickets with automatic amount calculation and daily cap.
- Recurring subscriptions (monthly, quarterly, yearly) with automatic invoicing, renewal and expiry reminders.
- Occupancy and revenue statistics per site.
- Automatic daily cron that invoices due subscriptions, renews them and raises reminders.
- Multi-company support with record rules per company.
- QWeb PDF reports: Parking Ticket, Subscription Contract, Revenue Report and Occupancy Report.

## Configuration

In Settings &gt; Parking you can configure:

- Default hourly rate.
- Default daily rate.
- Revenue account used to invoice subscriptions (falls back to the first income account of the company).

## Usage

1. Create sites, zones and places with capacity and rates.
2. Open a ticket at entry (reserves a place), close it at exit, mark it paid.
3. Create a subscription for recurring customers and activate it (reserves a place and generates the first invoice).
4. The daily cron invoices due subscriptions, renews them (extending the period) and raises reminders.
5. Use the Reports menu to print Revenue and Occupancy reports filtered by site and period.

## Permissions

- `sf_parking_management.group_sf_parking_user` - day-to-day operations.
- `sf_parking_management.group_sf_parking_manager` - full access and ticket cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.