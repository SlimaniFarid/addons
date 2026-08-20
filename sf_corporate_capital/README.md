# SF Corporate Capital

Shareholder Register & Capital Management (Cap Table) module for Odoo 18.

## Features

- Shareholder register with partner link and function.
- Share classes with nominal value and authorized shares.
- Capital movements (buy/sell) with quantity and unit price.
- Movement amount computed automatically.
- Issued shares per class computed from posted movements.
- Total shares and capital value per shareholder (cap table).
- Sell operations validated against current holdings.
- Posting workflow: Draft, Posted, Cancelled; posted movements are
  immutable.
- Multi-company support with record rules per company.
- QWeb PDF reports: Cap Table and Share Certificate.

## Installation

Copy the module folder into your Odoo addons path, update the module
list and install "Shareholder Register & Capital Management (Cap Table)".

## Usage

1. Create share classes under Corporate Capital &gt; Share Classes
   (nominal value, authorized shares).
2. Create shareholders under Corporate Capital &gt; Shareholders.
3. Record capital movements under Corporate Capital &gt; Capital
   Movements (buy/sell, quantity, unit price, date).
4. Post the movements; sell operations are checked against current
   holdings.
5. Issued shares and shareholder totals are updated automatically.
6. Use the Print menu to export the cap table or a share certificate.

## Permissions

- `sf_corporate_capital.group_sf_capital_user` - create shareholders,
  share classes and capital movements, post draft movements.
- `sf_corporate_capital.group_sf_capital_manager` - cancel posted
  movements, full access.

## Dependencies

- base, mail, contacts.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.