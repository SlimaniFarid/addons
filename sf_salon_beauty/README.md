# SF Salon Beauty

Salon &amp; Beauty Studio Management module for Odoo 18.

## Features

- Appointments with staff availability and conflict detection.
- Per-employee schedules and service history.
- Prepaid packages and memberships with session consumption.
- Automatic staff commission calculation per period.
- Automatic invoicing of completed services.
- Daily expiry handling for packages with activity alerts.
- Multi-company support with record rules per company.
- QWeb reports: Customer Card, Commissions Report and Activity Report.

> Note: counter product sales are not implemented in this module. The
> spec (§9 data model, MVP MUST) does not define a sale model; revenue is
> handled through automatic invoicing of completed services (account).

## Configuration

In Settings &gt; Salon you can configure:

- Default commission rate.
- Default service duration in minutes.

## Usage

1. Create services and staff members.
2. Book appointments with conflict checking.
3. Confirm, start and complete appointments; completed appointments generate invoices.
4. Sell prepaid packages and consume sessions on completion.
5. Compute monthly commissions per staff member.

## Permissions

- `sf_salon_beauty.group_sf_salon_user` - day-to-day operations.
- `sf_salon_beauty.group_sf_salon_manager` - full access, commission rates and package refunds.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.