# Automated Supplier Invoice Control (3-Way Match)

Automatic reconciliation of supplier invoices against purchase
orders and receipts: quantity, unit price, taxes and discounts,
with configurable tolerances and a full exception workflow.
Payment stays blocked while major discrepancies are unresolved.

## Features

- Automatic 3-way comparison: order, receipt, invoice
- Configurable tolerances per company (qty, price %, total %)
- Optional supplier-specific tolerances
- Statuses: pending / in_review / matched / exception / resolved /
  payment_blocked
- Exception workflow with responsible, decision and notes
- Validation and payment blocked while a major exception is open
- Full match history (sf.invoice.match.log)
- Dashboard of discrepancies by supplier

## Installation

Copy the module to your addons path, update the app list and
install **Automated Supplier Invoice Control (3-Way Match)**.

## Configuration

Assign the groups in Settings > Users:

- **Invoice Matching User**: consult controls and run matching.
- **Invoice Matching Manager**: arbitrate exceptions, configure
  tolerances, dashboard.

Company settings (Settings > 3-Way Match):
- Quantity tolerance (default 0).
- Price tolerance % (default 2).
- Total tolerance % (default 2).

Supplier-specific tolerances can be set on the supplier partner
(leave -1 to use the company default).

## Usage

1. Create a purchase order and confirm it.
2. Receive the goods (validated receipt).
3. Create the vendor bill. Its lines are linked to the PO lines.
4. Run 3-Way Match (button on the invoice or from the menu).
5. If major discrepancies are found, the invoice enters exception
   and payment is blocked.
6. Arbitrate the exception (accept or revise).
7. Recheck after correction to unblock.

## Permissions

- `sf_invoice_matching.group_invoice_matching_user` — read/limited.
- `sf_invoice_matching.group_invoice_matching_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- sale
- purchase
- purchase_stock
- account
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).