# SF Travel Agency

Travel agency management module for Odoo 18.

## Features

- Travel packages with destination, dates, price, capacity and providers.
- Providers grouped by type: hotel, transport, activity, insurance, other.
- Reservations with a full workflow: draft, confirmed, paid, completed, cancelled.
- Provider costs attached to reservations with automatic cost, commission and margin computation.
- Capacity control on packages.
- Daily cron alerts for imminent departures and long-unpaid confirmed reservations.
- Manager-only protections for price changes, cancellation of paid reservations and provider archiving.
- Multi-company support with record rules per company.
- QWeb reports: Reservation Confirmation, Package Itinerary, Reservation Invoice and Margin Report.

## Configuration

In Settings > Travel Agency you can configure:

- Default commission rate applied to reservations (default 10%).
- Number of days before departure used by the reminder cron (default 7).

## Usage

1. Create providers.
2. Create packages and attach providers.
3. Create reservations against packages.
4. Add provider costs on reservations to track cost, commission and margin.
5. Confirm, pay and complete reservations.
