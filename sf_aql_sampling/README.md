# SF AQL Sampling

Acceptance Sampling &amp; AQL Inspection Plans module for Odoo 18.

## Features

- Sampling plans (ISO 2859-1 style) with inspection level, lot size range, sample size and accept/reject numbers.
- Lot inspections (incoming, production, final) with automatic plan selection by lot size.
- Defect recording by severity (critical, major, minor) with weighted scoring (critical 10, major 5, minor 1).
- Automatic accept/reject decision based on the plan reject number (weighted or raw, configurable).
- Release or rejection of inspected lots (manager rights).
- Multi-company support with record rules per company.
- QWeb PDF report: AQL Inspection Report.

## Configuration

In Settings &gt; AQL Sampling you can configure:

- Default inspection level applied to new inspections.
- Whether defects are weighted by severity (enabled by default).

## Usage

1. Create sampling plans (level, lot size range, sample size, accept and reject numbers).
2. Create a lot inspection; the matching plan is proposed automatically from the lot quantity.
3. Record the defects found on the sample.
4. Complete the inspection; the decision (accepted / rejected) is computed automatically.
5. Release or reject the lot (requires manager rights).
6. Print the inspection report PDF from the form.

## Permissions

- `sf_aql_sampling.group_sf_aql_sampling_user` - plans, inspections and defect entry.
- `sf_aql_sampling.group_sf_aql_sampling_manager` - release, rejection and cancellation of inspections.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.