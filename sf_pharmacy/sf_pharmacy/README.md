# Pharmacy & Dispensation Management

Retail pharmacy management: pharmaceutical products, batch stock with
expiry dates, stock-out and expiry alerts, and traced prescription
dispensations. Handles batch recalls and stock movement tracking for
pharmacists, dispensers and stock managers.

## Features

- Pharmaceutical products with ATC code, dosage, form and price
- Batch stock with expiry dates and available quantity computed
- Prescriptions and dispensations traced per batch (FIFO by
  nearest expiry)
- Batch movements: receipts, dispensations, withdrawals, recalls
- Expiry and stock-out alerts (daily cron, deduplicated)
- Batch recalls identifying patients who received a recalled lot
- PDF reports: batch inventory, dispensations and stock valuation
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Pharmacy & Dispensation Management**.

## Configuration

Assign the groups in Settings > Users:

- **Pharmacy User**: products, batches, prescriptions and
  dispensations.
- **Pharmacy Manager**: batch withdrawal, recalls, inventory
  adjustments and purge.

Company settings (Settings > Pharmacy):
- Alert thresholds (expiry days, low stock level).

## Usage

1. Create products and receive batches with expiry dates.
2. Record a prescription and dispense quantities per batch.
3. Monitor the dashboard for expiring and out-of-stock products.
4. Withdraw recalled or expired lots (manager).
5. Launch a batch recall; affected patients are notified.
6. Generate PDF reports for inventory, dispensations and valuation.

## Permissions

- `sf_pharmacy.group_sf_pharmacy_user` — read/write on business
  models within the company.
- `sf_pharmacy.group_sf_pharmacy_manager` — reserved actions:
  batch withdrawal, recalls, adjustments and purge.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).
