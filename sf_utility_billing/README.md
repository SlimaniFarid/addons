# SF Utility Billing

Utility &amp; Sub-Meter Billing module for Odoo 18.

## Features

- Delivery points and meters registry (water, electricity, gas, heating).
- Reading campaigns with manual entry and CSV import (wizard, bulk index entry).
- Automatic consumption calculation from index difference, recalculated when prior
  readings are rejected or backdated.
- Tiered tariff grids applied on consumption ranges (per company, contiguous tiers).
- Consumption invoices with accounting posting and overdue tracking.
- Abnormal consumption detection with TODO activities (assigned to the operator).
- Multi-company support with record rules per company.
- QWeb reports: Consumption Reading, Campaign Report, Consumption Invoice and Overdue Invoices.

## Configuration

In Settings &gt; Utilities you can configure:

- Abnormal consumption threshold.
- Default revenue account for consumption invoices.

The revenue account is resolved per company: if the configured account belongs to
another company it is ignored and the first income account of the invoicing
company is used instead.

## Usage

1. Create meters for your delivery points.
2. Create a campaign, select meters and open it (readings are prepared).
3. Enter and validate readings; a decreasing index rejects the reading.
   Use "Import CSV" on the campaign (or the Readings &gt; Import Readings menu)
   to bulk-enter indexes: paste one line per reading (`meter,index,YYYY-MM-DD`,
   or `index,YYYY-MM-DD` when a meter is preselected; the date defaults to the
   campaign period end).
4. Configure a tariff grid with tiered prices (tiers must be contiguous).
5. Close the campaign: consumptions are calculated and invoices generated.
6. Post the invoices to create accounting moves; overdue invoices are flagged daily.

Rejecting a validated reading or cancelling an invoice requires the Manager group;
cancelling an invoice backed by a posted accounting move is blocked.

## Permissions

- `sf_utility_billing.group_sf_utility_user` - day-to-day operations.
- `sf_utility_billing.group_sf_utility_manager` - tariff modification, reading rejection and invoice cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.