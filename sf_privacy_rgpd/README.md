# Privacy & RGPD

Data protection register (RGPD) and privacy governance: treatments
(purposes, legal bases, retention), processors and DPA contracts,
impact assessments (AIPD) with risks and measures, breach register
(72 h notification) and data subject rights requests.

## Features

- Treatment register with workflow (draft to closed)
- Sequential numbering (PRT-, AIP-, BRH-, REQ-)
- Legal basis, data categories, retention and recipients per treatment
- Processors register with DPA contract and file
- Impact assessments (AIPD) with risk score and manager validation
- Breach register with 72 h notification deadline
- Data subject rights requests (access, erasure, portability...)
- Periodic review alerts via cron (configurable interval)
- Exportable treatment and breach registers (PDF)
- Privacy dashboard

## Installation

Copy the module to your addons path, update the app list and
install **Privacy & RGPD**.

## Configuration

Assign the groups in Settings > Users:

- **Privacy User**: register treatments, processors, breaches and
  requests.
- **Privacy Manager**: full access (validation of impact assessments,
  breach closure, configuration, dashboard).

Company settings (Settings > Privacy & RGPD):
- Treatment review interval (days, default 365).
- Breach notification deadline (hours, default 72).

## Usage

1. Register a treatment with purpose, legal basis, data categories,
   retention and recipients.
2. Record processors and their DPA contracts.
3. Submit an impact assessment; the manager validates or rejects it.
4. Detect, declare, remediate and close breaches (closure requires
   remediation measures).
5. Track data subject rights requests until closure.

## Permissions

- `sf_privacy_rgpd.group_privacy_user` — read/write limited.
- `sf_privacy_rgpd.group_privacy_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).