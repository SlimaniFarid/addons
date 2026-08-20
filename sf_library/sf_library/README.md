# Library & Media Center Management

Structured catalogue of items and media (books, DVDs, CDs, games,
press), members, dated loans and returns with availability
tracking, computed late days and fines, reservations with
availability lifting and cron alerts.

## Features

- Item catalogue with media types and categories
- Members / users with statuses (draft, active, blocked)
- Loans and returns with available copies computed
- Late days and late fees automatically computed
- Reservations lifted when an item becomes available
- Daily cron alerts for late loans and expiring reservations
- PDF reports: loan receipt / member card, late loans & sanctions
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Library & Media Center Management**.

## Configuration

Assign the groups in Settings > Users:

- **Library User**: catalogue, members, loans and reservations.
- **Library Manager**: returns, member blocking, reservation
  lifting and cancellations.

Company settings (Settings > Library):
- Loan duration, fine per day and hold days.

## Usage

1. Build the catalogue with items and categories.
2. Register members (patrons).
3. Record a loan if an available copy exists.
4. Return a document; late days and fees are computed.
5. Reserve unavailable items; reservations are lifted on
   availability.
6. The cron alerts overdue loans and expiring reservations.

## Permissions

- `sf_library.group_sf_library_user` — catalogue, members, loans
  and reservations.
- `sf_library.group_sf_library_manager` — returns, member blocking,
  reservation lifting and cancellation.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).
