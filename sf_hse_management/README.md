# HSE — Health & Safety Management

Centralize your occupational health and safety program with
incident management, inspections, risk assessments, work permits
and PPE tracking.

## Features

- Incident declaration (accident, near miss, property damage,
  environmental) with severity levels and attachments
- Investigation workflow with root cause analysis
- Corrective and preventive action plans with owners and due dates
- Inspections with reusable checklists and non-conformity detection
- Risk assessment with a 5x5 probability x severity matrix
  (low / medium / high / extreme)
- Work permits (fire, confined space, height, hot work,
  excavation) with approval workflow
- PPE tracking with assignment and expiry alerts
- Days without accident tracking per company

## Installation

Copy the module to your addons path, update the app list and
install **HSE — Health & Safety Management**.

## Configuration

No mandatory configuration. Assign the groups in Settings >
Users:

- **HSE User**: declare incidents and request permits.
- **HSE Manager**: full access (investigations, inspections,
  risks, permits approval, PPE, configuration).

## Usage

1. Declare an incident, start the investigation, define
   corrective actions and resolve/close the file.
2. Run inspections from reusable checklists.
3. Register risks; the risk level is computed automatically.
4. Request and approve work permits.
5. Track PPE assignments and expirations.

## Permissions

- `sf_hse_management.group_hse_user` — read/write limited.
- `sf_hse_management.group_hse_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- hr

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).