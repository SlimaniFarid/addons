# Insurance & Claims Management

Centralize the company insurance program: insurers, policies with
guarantees, premiums and maturities, automatic renewals, claims with
declaration and follow-up up to indemnification and a dashboard of the
whole insurance program per company.

## Features

- Insurers and intermediaries reference (partner linked)
- Policies with sequential numbering (POL-xxxx)
- Guarantees per policy (coverage, deductible)
- Premiums with amount and frequency
- Policy workflow: draft → active → under review → expired / cancelled
- Automatic expiry and renewal via cron
- Claims with sequential numbering (CLA-xxxx)
- Claim workflow: draft → declared → under review → estimated →
  settled / rejected
- Settlement amount control (warning when above the estimation)
- Renewal and declaration reminder activities (configurable delay)
- Insurance Program and Claims Report PDF
- Dashboard of policies by type and status

## Installation

Copy the module to your addons path, update the app list and
install **Insurance & Claims Management**.

## Configuration

Assign the groups in Settings > Users:

- **Insurance Management User**: create and manage insurers, policies,
  guarantees and claims.
- **Insurance Management Manager**: full access, including settling and
  rejecting claims.

Company settings (Settings > Insurance Management):
- Renewal reminder delay (days) before the end date.

## Usage

1. Create insurers and, optionally, link them to a partner.
2. Create a policy with type, dates, premium, guarantees and
   automatic renewal if needed.
3. Activate the policy; the cron expires it at the end date or creates
   the next period automatically.
4. Declare claims on the policy and follow the status up to the
   indemnity.
5. Use the Insurance Program and Claims Report PDFs and the dashboard.

## Permissions

- `sf_insurance_management.group_insurance_user` — read/write limited.
- `sf_insurance_management.group_insurance_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).