# Risk Management

Governance, risk and compliance for NIS2, DORA, ISO 27001, GDPR
and internal control frameworks.

## Features

- Centralized risk register with categories, sources and owners
- 5x5 probability x impact matrix with automatic risk class
  (low / medium / high / extreme) and residual risk
- Treatment plans with actions, owners, due dates and evidence
- Control catalog with frequency and pass/fail test history
- Regulatory requirement mapping (NIS2, DORA, ISO 27001, GDPR,
  ISO 9001)
- Risk heatmap and register dashboards
- Audit-ready reports

## Installation

Copy the module to your addons path, update the app list and
install **GRC — Enterprise Risk Management**.

## Configuration

Assign the groups in Settings > Users:

- **GRC User**: declare risks and manage their own actions.
- **GRC Manager**: full access (assessments, treatments, controls,
  requirements, configuration).

## Usage

1. Create a risk and assess it (probability x impact).
2. Define a treatment plan and start monitoring.
3. Register controls and run periodic tests.
4. Map regulatory requirements to risks.
5. Consult the heatmap and reports for audits.

## Permissions

- `sf_risk_management.group_risk_user` — read/write limited.
- `sf_risk_management.group_risk_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- hr (departments)

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).