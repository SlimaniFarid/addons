# ESG Reporting (CSRD)

Collect and report ESG indicators (environment, social, governance) per
company and period for CSRD compliance: configurable indicator
repository, period validation workflow, automatic variation and target
achievement, PDF report and CSV export.

## Features

- Configurable ESG indicator repository (category, unit, direction, frequency)
- Sequential indicator and period numbering (KPI-xxxx, ESG-YYYY-Pxx)
- Periods with a validation workflow (draft -> submitted -> approved -> closed)
- Values per company and period with target
- Automatic variation vs previous period and target achievement (value/target)
- ESG PDF report per company and period
- CSV export of collected values
- Dashboard of values by indicator category

## Installation

Copy the module to your addons path, update the app list and install
**ESG Reporting (CSRD)**.

## Configuration

Assign the groups in Settings > Users:

- **ESG Reporting User**: collect values, manage indicators and periods.
- **ESG Reporting Manager**: full access (validation, reports, dashboard).

Company settings (Settings > ESG Reporting):
- Default period frequency.
- ESG reporting company flag.

## Usage

1. Create ESG indicators (category, unit, direction, frequency).
2. Create a collection period for the company.
3. Enter the values per indicator with optional targets.
4. Submit the period; a manager approves it: variation vs previous
   period and target achievement are computed and stored.
5. Export the ESG PDF report or the CSV of values.

## Permissions

- `sf_esg_reporting.group_esg_user` — read/write limited, no validation.
- `sf_esg_reporting.group_esg_manager` — full access, validates periods.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).