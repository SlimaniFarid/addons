# SF Policy Acknowledgment

Company Policy & Employee Acknowledgment Register module for Odoo 18.

## Features

- Versioned internal policies (category: Code of Conduct, Human Resources, IT Security, Safety, Data Protection, Finance, Quality, Other; version, effective and expiry dates, owner, content).
- Employee assignment per policy.
- Publication workflow: Draft, Published, Retired, Archived.
- Acknowledgment register generated at publication, one acknowledgment
  per assigned employee.
- Acknowledgment sign-off with date and user tracking.
- Acknowledgment coverage rate computed automatically.
- Automatic reminders for pending acknowledgments and for expiring
  policies (configurable number of days before expiry).
- Multi-company support with record rules per company.
- QWeb PDF reports: Policy report and Acknowledgment Register.

## Installation

Copy the module folder into your Odoo addons path, update the module
list and install "Company Policy & Employee Acknowledgment Register".

## Configuration

In Settings &gt; Policy Acknowledgment you can configure:

- Expiry reminder (number of days before expiry a reminder activity is
  raised, default 30).

## Usage

1. Managers create policies under Policy Acknowledgment &gt; Company
   Policies (category, version, dates, content, assigned employees).
2. Publish the policy: one acknowledgment is generated per assigned
   employee.
3. Employees open their pending acknowledgment and sign it (Acknowledge
   button).
4. The coverage rate is shown on the policy.
5. Daily crons raise reminders for pending acknowledgments and for
   policies close to their expiry date.
6. Use the Print menu to export the policy report or the acknowledgment
   register.

## Permissions

- `sf_policy_acknowledgment.group_sf_policy_user` - read policies and
  acknowledge own pending acknowledgments.
- `sf_policy_acknowledgment.group_sf_policy_manager` - create, publish,
  retire and archive policies, full access.

## Dependencies

- base, mail, contacts, hr.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.