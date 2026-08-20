# SF Laundry

Laundry &amp; Dry Cleaning Management module for Odoo 18.

## Features

- Deposit vouchers with customer details and item lists.
- Item-level tracking: received, in progress, ready, delivered, lost.
- Per-piece pricing by item type and service, with default prices from item types.
- Automatic expected delivery date from settings (default 3 days).
- Pickup and delivery timestamps.
- Daily cron alerts for overdue orders and slow in-progress items.
- Multi-company support with record rules per company.
- QWeb reports: Deposit Receipt, Delivery Ticket, Activity Report and Overdue Orders List.

## Configuration

In Settings > Laundry you can configure:

- Default delivery delay in days (default 3).
- Slow treatment threshold in hours (default 72).

## Usage

1. Create a laundry order with customer details.
2. Add items with type, service and quantity; unit prices are filled automatically from item types.
3. Receive the order, start treatment, mark items ready.
4. Handle lost items with regularize action.
5. Deliver the order to print the delivery ticket.

## Permissions

- `sf_laundry.group_sf_laundry_user` - day-to-day operations.
- `sf_laundry.group_sf_laundry_manager` - full access, price changes and order cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.