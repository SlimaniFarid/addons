# SF Business Travel

Corporate Business Travel Management module for Odoo 18.

## Features

- Travel requests with purpose, destination, dates, budget and justification.
- Hierarchical approval workflow: Draft, Submitted, Approved, Rejected, In Progress, Completed, Cancelled.
- Itinerary lines (flight, train, hotel, car, other) with estimated costs.
- Estimated cost computed from the itinerary lines and compared to the budget.
- Automatic departure reminders (configurable number of days before departure).
- Multi-company support with record rules per company.
- QWeb PDF reports: Travel Authorization (mission order) and Travel Itinerary.

## Installation

Copy the module folder into your Odoo addons path, update the module
list and install "Corporate Business Travel Management".

## Configuration

In Settings &gt; Business Travel you can configure:

- Departure reminder (number of days before departure a reminder
  activity is raised, default 2).

## Usage

1. Employees create travel requests under Business Travel &gt; Travel
   Requests (purpose, destination, dates, budget).
2. Submit the request; managers approve or reject it.
3. Detail the itinerary in the Itinerary tab (flights, hotels, etc.).
4. Start the travel at departure and complete it at return.
5. The daily cron raises departure reminders for upcoming approved
   travels.
6. Use the Print menu to export the travel authorization (mission
   order) or the itinerary.

## Permissions

- `sf_business_travel.group_sf_business_travel_user` - create and submit
  travel requests, manage own requests.
- `sf_business_travel.group_sf_business_travel_manager` - approve,
  reject and cancel requests, full access.

## Dependencies

- base, mail, contacts.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.