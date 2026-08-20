# Dock & Shipment Appointment Scheduling

Dock registry and truck appointment scheduling for warehouses, distribution centers and 3PL providers.

## Features

- Dock registry (receiving / shipping / both) with location and activity flag.
- Truck appointment scheduling with configurable time windows (default 60 minutes).
- Overlap detection: appointments on the same dock with overlapping windows are rejected.
- State workflow: Scheduled, Arrived, Docked, Completed, No-Show, Cancelled.
- Actual arrival / dock / departure timestamps with automatic delay and dock-duration computation.
- Daily cron that flags overdue scheduled appointments as No-Show and schedules a follow-up activity.
- Cancellation restricted to managers.
- Multi-company support with record rules per company.
- QWeb PDF report: Dock Appointment Schedule.

## Configuration

In Settings &gt; Dock Appointments:

- No-Show Grace (Minutes): tolerance after the appointment window before the cron marks a No-Show (default 15).
- Default Appointment Window (Minutes): window used for new appointments (default 60).

## Usage

1. Create docks (name, type, location).
2. Create an appointment with carrier, dock, direction, appointment datetime and window.
3. Register arrival when the truck shows up, then move to dock, then complete on departure.
4. Overdue appointments are flagged No-Show by the daily cron; the carrier can be contacted from the follow-up activity.

## Permissions

- `sf_dock_appointments.group_sf_dock_appointments_user` - docks and appointments.
- `sf_dock_appointments.group_sf_dock_appointments_manager` - cancellation of appointments.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.