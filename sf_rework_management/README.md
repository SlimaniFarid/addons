# Rework Management

Rework order tracking for manufacturing and quality departments.

## Features

- Rework orders linked to products and lots with quantity and source (inspection, customer return, internal, other).
- Common rework reasons (defective component, finish defect, assembly error, calibration, damage).
- Rework operations with hours and operator assignment.
- Scrap registration with automatic value from the product standard price.
- Automatic cost computation: total hours, labor cost, scrap value and total rework cost.
- Workflow: Draft, In Progress, Completed, Closed, Cancelled.
- Daily cron escalation alert when rework orders stay open longer than the configured days.
- Closing and cancellation restricted to managers.
- Multi-company support with record rules per company.
- QWeb PDF report: Rework Order.

## Configuration

In Settings &gt; Rework Management:

- Escalation Alert After (Days): alert when a rework order stays in progress for more than this many days (default 7).
- Default Hourly Rate: used for new rework orders (default 0).

## Usage

1. Create a rework order with product, quantity and source.
2. Start the order, then record operations and scrap as work is performed.
3. Costs are computed automatically from hours, hourly rate and scrap values.
4. Complete the order, then a manager closes it.
5. Long-running orders trigger an escalation activity via the daily cron.

## Permissions

- `sf_rework_management.group_sf_rework_management_user` - rework orders, operations and scrap.
- `sf_rework_management.group_sf_rework_management_manager` - closing and cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.