# Production Master Scheduling (MPS)

Plan production by work center and period, schedule manufacturing
orders with priorities, visualize the schedule in a Gantt view and
monitor the load per work center.

## Features

- Master production plans over a period with workflow
  (draft → confirmed → closed)
- Plan lines per work center, product and dates
- Load manufacturing orders (MRP) into the plan
- Gantt scheduling view colored by priority
- Work center load calculation
- Plan confirmation and closure

## Installation

Copy the module into your addons path, update the apps list and
install **Production Master Scheduling (MPS)**.

## Configuration

Settings → General Settings → Production Planning:

- **Load only draft manufacturing orders**: only include orders in
  draft state when loading MOs.

Create your plans under **Production Planning → Master Production
Schedules**, load MOs or add lines manually, then confirm the plan.

## Permissions

- **Production Planning User**: view and create plans and lines of
  their own company.
- **Production Planning Manager**: everything, including plan
  confirmation and multi-company access.

## Dependencies

- base
- mail
- mrp

## Compatibility

- Odoo 18.0 and 19.0
- Community and Enterprise