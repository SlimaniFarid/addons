# Fuel & Fleet Management

Manage the vehicle fuel fleet: vehicles and fuel cards, fills
(volume, price, mileage) with automatic L/100km consumption
calculation, tanks with gauge and receipts per site, anomaly
alerts and monthly PDF reports per vehicle.

## Features

- Vehicle and fuel card registry (diesel, gasoline, electric, LPG...)
- Sequential numbering (VEH-, CRD-, FUL-, TNK-, RCP-)
- Fuel fills with automatic total and L/100km consumption
- Tanks with current level and receipts per site
- Daily cron alerts: cards near expiry and abnormal fills
- Manager-only card blocking and fill validation
- Monthly consumption PDF report per vehicle
- Tank monitoring PDF report
- Multi-company record rules and dashboard by vehicle

## Installation

Copy the module to your addons path, update the app list and
install **Fuel & Fleet Management**.

## Configuration

Assign the groups in Settings > Users:

- **Fuel Management User**: register vehicles, cards, fills,
  tanks and receipts.
- **Fuel Management Manager**: full access (card blocking,
  fill validation, reports).

Company settings (Settings > Fuel Management):
- Expiry alert (days).
- Maximum consumption (L/100km).

## Usage

1. Create vehicles and assign fuel cards.
2. Record fuel fills (date, volume, price, odometer); the total
   and the L/100km consumption are computed automatically.
3. Manage tanks per site and record receipts.
4. The daily cron raises activities for cards near expiry and
   abnormal consumption.
5. Print the monthly consumption report per vehicle or the tank
   monitoring report.

## Permissions

- `sf_fuel_management.group_fuel_user` — read/write limited.
- `sf_fuel_management.group_fuel_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).