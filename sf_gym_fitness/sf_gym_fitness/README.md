# Gym & Fitness Management

Sports subscriptions with plans and prices, group classes with
planning and coaches, member attendances, membership payments and
cron alerts for expiring subscriptions and under-filled sessions.

## Features

- Members with contact details, birth date and photo
- Membership plans with monthly price and duration
- Group lessons with maximum capacity per session
- Session planning with coaches and attendance tracking
- Subscription payments and automatic paid status
- Automatic alerts for expiring subscriptions and empty
  sessions (cron, deduplicated)
- PDF reports: subscription contract and session planning
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Gym & Fitness Management**.

## Configuration

Assign the groups in Settings > Users:

- **Gym User**: members, subscriptions, sessions and
  attendances.
- **Gym Manager**: plans, formulas, advanced session statuses
  and payments.

Company settings (Settings > Gym):
- Number of days before an expiring subscription is reminded.

## Usage

1. Create a membership plan with monthly price and duration.
2. Register members and subscribe them to a plan.
3. Plan group class sessions and assign coaches.
4. Record attendances per session.
5. Receive subscription payments; the subscription is marked
   paid.
6. The cron alerts expiring subscriptions and empty sessions.

## Permissions

- `sf_gym_fitness.group_gym_user` — members, subscriptions,
  sessions and attendances.
- `sf_gym_fitness.group_gym_manager` — plans, formulas, advanced
  session statuses and payments.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).
