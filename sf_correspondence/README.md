# SF Correspondence

Business Mail &amp; Correspondence Register module for Odoo 18.

## Features

- Incoming and outgoing correspondence register with direction, date, correspondent, subject and reference.
- Routing to an internal department and an assigned responsible person.
- Status workflow: Draft, Open, In Progress, Responded, Archived, Cancelled.
- Response deadlines with automatic daily reminders (configurable lead time).
- Registered mail tracking with acknowledgment flag.
- Scanned attachments stored on each correspondence.
- Multi-company support with record rules per company.
- QWeb PDF reports: Correspondence Register and Correspondence Sheet.

## Installation

Copy the module folder into your Odoo addons path, update the module
list and install "Business Mail &amp; Correspondence Register".

## Configuration

In Settings &gt; Correspondence you can configure:

- Response reminder (number of days before the due date the reminder
  is raised, default 2).

## Usage

1. Create your internal departments under Correspondence &gt; Departments.
2. Record incoming or outgoing mail under Correspondence &gt;
   Correspondence Register (direction, correspondent, subject, dates).
3. Route the record to a department and a responsible person and set
   the response due date.
4. Follow the status: Open, In Progress, Responded, Archive.
5. The daily cron creates reminder activities for correspondence whose
   response is due.
6. Use the Print menu to export the correspondence register or a single
   correspondence sheet.

## Permissions

- `sf_correspondence.group_sf_correspondence_user` - day-to-day operations.
- `sf_correspondence.group_sf_correspondence_manager` - full access,
  cancellation and deletion.

## Dependencies

- base, mail, contacts.

## Compatibility

- Odoo 18: supported.
- Odoo 19: compatible (identical architecture).

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.