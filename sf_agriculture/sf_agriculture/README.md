# Agriculture Management & Farm Operations

Manage farms and cooperatives: farms and plots (surface, soil),
agricultural campaigns, cultures and technical itineraries,
treatments (crop protection, fertilizers) with withdrawal periods,
harvests with yield computation, inputs register and campaign
reports in PDF.

## Features

- Farm and plot reference data (surface in hectares, soil, irrigation)
- Sequential numbering for farms, plots, campaigns, cultures,
  treatments and harvests
- Agricultural campaigns with cultures assigned to plots
- Technical itineraries (operations) per culture
- Treatments with withdrawal periods and automated alerts (cron)
- Harvests with yield calculation (t/ha)
- Inputs register and campaign reports in PDF
- Dashboard of yields by crop

## Installation

Copy the module to your addons path, update the app list and
install **Agriculture Management & Farm Operations**.

## Configuration

Assign the groups in Settings > Users:

- **Agriculture User**: farms, plots, campaigns, cultures,
  treatments and harvests.
- **Agriculture Manager**: full access, closing campaigns and
  recording harvests, all companies.

Company settings (Settings > Agriculture):
- Default harvest unit (kg or tonnes).

## Usage

1. Create a farm and its plots (area in hectares, soil, irrigation).
2. Open a campaign and assign cultures to plots.
3. Record treatments (crop protection, fertilizers) with product and
   withdrawal period.
4. Register harvests; the yield (t/ha) is computed automatically.
5. Print the inputs register and campaign reports in PDF.

## Permissions

- `sf_agriculture.group_agri_user` — read/write limited.
- `sf_agriculture.group_agri_manager` — full access, closing
  campaigns and recording harvests.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).