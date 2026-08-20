# Packaging Consigns Management

Manage returnable packaging and consigns for distributors, breweries
and producers: deposit packaging types, parks per site, emissions and
returns linked to deliveries, invoiced consigns, computed return rate
and stock alerts.

## Features

- Deposit packaging types (deposit amount, units per lot)
- Parks per site with computed available quantity
- Emissions and returns linked to deliveries (reference)
- Invoiced consigns via deposit_total computation
- Return rate computed per park (returns / emissions)
- Daily cron alerts when a park is below the minimum stock
- Consignment follow-up and parks status PDF reports
- Multi-company record rules and dedicated user / manager groups

## Installation

Copy the module to your addons path, update the app list and
install **Packaging Consigns Management**.

## Configuration

Assign the groups in Settings > Users:

- **Packaging Consigns User**: record emissions and returns, parks.
- **Packaging Consigns Manager**: full access (validating/checking
  moves and returns, configuration).

Company settings (Settings > Packaging Consigns):
- Park alert tolerance (days).

## Usage

1. Create deposit packaging types (deposit amount, units per lot,
   minimum stock).
2. Create sites and their managers.
3. Record emissions; validating a move automatically creates or
   updates the park of the packaging type and site.
4. Record returns; a return cannot exceed the partner's outstanding
   consigned balance.
5. Parks show the available quantity and the return rate.
6. Run the cron or the follow-up / parks status PDF reports.

## Permissions

- `sf_packaging_consigns.group_packaging_user` — read/write limited.
- `sf_packaging_consigns.group_packaging_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).