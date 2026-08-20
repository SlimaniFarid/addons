# SF Gifts &amp; Hospitality

Corporate Gifts &amp; Hospitality Register module for Odoo 18.

## Features

- Declaration of gifts, hospitality and invitations given or received by employees.
- Automatic computation of whether an approval is required (configurable threshold).
- Approval workflow: Draft, Submitted, Approved, Rejected, Archived.
- Auto-approval of declarations below the threshold (self-declared).
- Annual register per employee with total per year.
- Multi-company support with record rules per company.
- QWeb PDF reports: Gifts Register and Annual Declaration.

## Installation

Copy the module folder into your Odoo addons path, update the module
list and install "Corporate Gifts &amp; Hospitality Register".

## Configuration

In Settings &gt; Gifts &amp; Hospitality you can configure:

- Approval threshold: any declaration whose estimated value is equal
  to or above the threshold must be approved by a manager.

## Usage

1. Employees declare every gift or hospitality given or received
   (direction, date, category, estimated value, justification).
2. If the value is below the threshold, submitting the declaration
   auto-approves it (declared).
3. Otherwise the declaration is submitted and must be approved or
   rejected by a manager.
4. Use the Print menu to export the gifts register or the annual
   declaration grouped per employee.

## Permissions

- `sf_gifts_hospitality.group_sf_gifts_hospitality_user` - declare gifts
  and resubmit rejected declarations.
- `sf_gifts_hospitality.group_sf_gifts_hospitality_manager` - approve,
  reject, archive and delete declarations.

## Dependencies

- base, mail, contacts.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.