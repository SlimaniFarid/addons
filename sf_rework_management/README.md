# Rework Management

Rework order tracking for manufacturing and quality departments.

## Features

- Rework orders linked to products and lots with quantity and source (production, quality, customer_return, other).
- Free-text reason field for rework orders.
- Disposition decisions: rework, scrap, use_as_is, return_to_supplier, other.
- Rework operations with hours, operator (name and user), hourly rate per operation, and notes.
- Scrap registration with unit value and scrap reason; value computed as qty x unit_value.
- Multi-currency support: all monetary fields use currency_id from company.
- Automatic cost computation: total hours, labor cost (sum of hours x hourly_rate per operation), scrap value and total rework cost.
- Workflow: Draft, In Progress, Completed, Closed, Cancelled.
- Daily cron escalation alert when rework orders (draft or in_progress) stay open longer than configured days.
- Write guard: completed/closed/cancelled orders cannot be modified except by manager with context.
- Closing and cancellation restricted to managers.
- Multi-company support with record rules per company.
- QWeb PDF report: Rework Order.

## Configuration

In Settings > Rework Management:

- Escalation Alert After (Days): alert when a rework order stays in draft or in progress for more than this many days (default 7).
- Default Hourly Rate: used for new rework orders (default 0).

## Usage

1. Create a rework order with product, quantity, source, reason, and hourly rate.
2. Start the order, then record operations (with hours, hourly rate, operator) and scrap (with qty, unit_value, scrap_reason) as work is performed.
3. Costs are computed automatically from operations (hours x hourly_rate) and scrap (qty x unit_value).
4. Complete the order, then a manager closes it.
5. Long-running orders (draft or in_progress) trigger an escalation activity via the daily cron.

## Permissions

- `sf_rework_management.group_sf_rework_management_user` - rework orders, operations and scrap.
- `sf_rework_management.group_sf_rework_management_manager` - closing, cancellation, and write access on locked states.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.