# SF Corporate Capital

Shareholder Register & Capital Management (Cap Table) module for Odoo 18.

## Features

- Shareholder register with partner link and shareholder type (individual/company).
- Share classes with nominal value and authorized shares (default 0).
- Capital movements with three types: Issue, Transfer, Buyback.
  - Issue: creates new shares for a shareholder (+ issued shares).
  - Transfer: moves shares between two shareholders (- from, + to, no change to issued).
  - Buyback: company repurchases shares from a shareholder (- issued shares).
- Movement amount computed automatically (quantity × unit price).
- Issued shares per class computed from posted movements.
- Total shares and capital value per shareholder (cap table).
- Sell/buyback/transfer operations validated against current holdings.
- Posting workflow: Draft, Posted, Cancelled; posted movements are immutable.
- Post and Cancel actions reserved to Capital Manager group.
- Multi-company support with record rules per company.
- Settings: default nominal value and default authorized shares for new share classes.
- QWeb PDF reports: Cap Table (per class with quantities, %, totals) and Share Certificate (aggregated attestation per shareholder/class).

## Installation

Copy the module folder into your Odoo addons path, update the module list and install "Shareholder Register & Capital Management (Cap Table)".

## Usage

1. Configure defaults under Settings → Corporate Capital (default nominal value, default authorized shares).
2. Create share classes under Corporate Capital → Share Classes (nominal value, authorized shares).
3. Create shareholders under Corporate Capital → Shareholders (partner, type: individual/company).
4. Record capital movements under Corporate Capital → Capital Movements:
   - Issue: select shareholder, share class, quantity, unit price.
   - Transfer: select from shareholder, to shareholder, share class, quantity.
   - Buyback: select shareholder, share class, quantity, unit price.
5. Post the movements (manager only); validations check holdings.
6. Issued shares and shareholder totals are updated automatically.
7. Use the Print menu to export the cap table or a share certificate.

## Permissions

- `sf_corporate_capital.group_sf_capital_user` - create shareholders, share classes and capital movements, view reports.
- `sf_corporate_capital.group_sf_capital_manager` - post and cancel movements, full access, configure defaults.

## Scope & Differences

This module covers the **shareholder register, share classes, and capital movements (cap table)**.

- **sf_investment_management**: manages investment rounds, term sheets, cap table scenarios, dilution modeling — broader equity management for fundraising.
- **sf_corporate_secretary**: manages board meetings, resolutions, statutory registers, compliance filings — corporate governance and legal secretarial duties.

This module focuses on the **operational register of shareholders and share movements**; it does not handle investment scenarios or corporate governance acts.

## Dependencies

- base, mail, contacts.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.