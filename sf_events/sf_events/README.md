# SF Events

Events &amp; Conferences Management module for Odoo 18.

## Features

- Events with dates, locations, capacities and budgets.
- Sessions with speakers, rooms and schedules.
- Registrations and ticketing with ticket types and capacity control.
- Badge check-in with timestamps.
- Budget and revenue tracking per event.
- Daily cron alerts for upcoming events and negative budget balances.
- Multi-company support with record rules per company.
- QWeb reports: Event Program, Registration Confirmation, Budget Report and Attendance Report.

## Configuration

In Settings > Events you can configure:

- Number of days before an event used by the reminder cron (default 7).

## Usage

1. Create an event with dates, location, capacity and budget.
2. Create sessions and assign speakers.
3. Register attendees with ticket types and prices.
4. Check in badges when the event is in progress.
5. Track expenses and review budget, revenue and balance.

## Permissions

- `sf_events.group_sf_events_user` - read/write limited.
- `sf_events.group_sf_events_manager` - full access, event cancellation and budget changes.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.