# Donations & Charity Management

Manage donation campaigns (target and collected amounts), pledges
(one-time or monthly), received payments and fiscal receipts, with
automatic reminders for unpaid pledges.

## Features

- Donation campaigns with target and collected amounts
- Sequential numbering for campaigns, pledges, payments and receipts
- Pledges (one-time / monthly) linked to campaigns
- Payments received with collected amount computed per campaign
- Fiscal receipts issued by managers
- Automatic reminders for overdue unpaid pledges (cron)
- PDF report per campaign and fiscal receipts register
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Donations & Charity Management**.

## Configuration

Assign the groups in Settings > Users:

- **Donations User**: campaigns, pledges and payments.
- **Donations Manager**: full access, receiving payments and
  issuing fiscal receipts, all companies.

Company settings (Settings > Donations):
- Number of days before an unpaid pledge is reminded.

## Usage

1. Create a donation campaign with target and dates.
2. Record pledges (one-time or monthly) from donors.
3. Receive payments; the campaign collected amount updates
   automatically.
4. Issue fiscal receipts (manager).
5. The cron reminds unpaid overdue pledges.

## Permissions

- `sf_donations.group_sf_donation_user` — read/write limited.
- `sf_donations.group_sf_donation_manager` — full access, receiving
  payments and issuing receipts.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).