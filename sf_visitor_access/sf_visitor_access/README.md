# Visitor Management & Site Access

Manage visitors and contractors on site: check-in / check-out,
visit types, badges and authorized zones, accepted safety rules
(waiver), overtime alerts and a real-time presence register.

## Features

- Visitor register with check-in / check-out
- Sequential visit numbering (VIS-xxxx)
- Unique badge generation at check-in
- Authorized zones and authorized duration per visit
- Safety rules acceptance (waiver) per site, versioned
- Overtime alerts via cron (configurable threshold)
- Real-time "Present on site" list for evacuation
- Known recurring visitors
- Dashboard of visits by type and gate

## Installation

Copy the module to your addons path, update the app list and
install **Visitor Management & Site Access**.

## Configuration

Assign the groups in Settings > Users:

- **Visitor Access User**: register visits, check-in/out, register.
- **Visitor Access Manager**: full access (sites, rules,
  configuration, dashboard).

Company settings (Settings > Visitor Access):
- Overtime alert delay (hours).

## Usage

1. Create sites / access points and their safety rules.
2. Pre-register a planned visit or check in directly.
3. Check in: a badge is generated and the safety waiver must be
   accepted when the site has rules.
4. Check out on departure; archive the visit.
5. Use "Present on Site" for a real-time list (evacuation).

## Permissions

- `sf_visitor_access.group_visitor_user` — read/write limited.
- `sf_visitor_access.group_visitor_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- hr
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).