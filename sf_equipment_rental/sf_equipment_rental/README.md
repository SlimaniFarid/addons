# SF Equipment Rental

Equipment Rental &amp; Hire Operations module for Odoo 18.

## Features

- Equipment cards with serial, purchase value and tiered prices.
- Rental contracts with tiered pricing (hour/day/week/month).
- Availability conflict detection across confirmed and active contracts.
- Out and in inspections with condition and damage records.
- Penalties added to contracts from return inspections.
- Maintenance planning that makes equipment unavailable.
- Automatic invoicing of returned contracts.
- Multi-company support with record rules per company.
- QWeb reports: Rental Contract, Out / In Ticket and Fleet Report.

## Configuration

In Settings &gt; Rental you can configure:

- Penalty account for damage penalties.

## Usage

1. Create equipment and categories with tiered prices.
2. Create a contract with equipment lines, period and tier pricing.
3. Confirm the contract (conflict check), start the rental with out inspection.
4. Complete return inspections with damages and penalties.
5. Return, invoice and close the contract.
6. Plan maintenance to keep the fleet in good condition.

## Permissions

- `sf_equipment_rental.group_sf_rental_user` - day-to-day operations.
- `sf_equipment_rental.group_sf_rental_manager` - full access, contract cancellation and discounts.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.