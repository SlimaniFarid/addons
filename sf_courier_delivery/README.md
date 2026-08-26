# SF Courier Delivery

Courier &amp; Parcel Delivery Management module for Odoo 18.

## Features

- Pickup/delivery requests with addresses and time windows.
- Courier assignment and daily route planning.
- Delivery tracking: to collect, assigned, in transit, delivered, failed, returned.
- Proof of delivery (signature or photo) with timestamp.
- Delivery failure handling with retry and return flow.
- Automatic daily alerts for overdue and unresolved deliveries.
- Multi-company support with record rules per company.
- QWeb reports: Delivery Ticket, Collection Note, Disputes List and Activity Report.

## Configuration

In Settings &gt; Courier you can configure:

- Default delivery price.

## Usage

1. Create a courier request with customer and addresses.
2. Confirm the request and create deliveries for it.
3. Assign a courier, plan a route and start the deliveries.
4. Capture the proof of delivery on completion.
5. Handle failures with retry or return.

## Permissions

- `sf_courier_delivery.group_sf_courier_user` - day-to-day operations.
- `sf_courier_delivery.group_sf_courier_manager` - full access and delivery cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.