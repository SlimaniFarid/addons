# Cold Chain Monitoring

Temperature excursion monitoring for cold storage sites and refrigerated transport.

## Features

- Cold storage sites with type (cold storage, chamber, freezer, cold room, refrigerated transport) and temperature range.
- Transport trips with carrier, vehicle, planned/actual departure and arrival, and temperature range.
- Temperature readings linked to a trip or a site with automatic range check.
- Automatic excursion detection: an out-of-range reading opens (or reuses) an excursion linked to the source.
- Excursion analytics: duration, maximum deviation and severity (low / medium / high).
- Manager-only excursion resolution with resolution note and timestamps.
- Daily cron escalation alert when excursions stay unresolved beyond the configured hours.
- Multi-company support with record rules per company.
- QWeb PDF report: Cold Chain Log.

## Configuration

In Settings &gt; Cold Chain:

- Unresolved Excursion Alert After (Hours): alert when an excursion stays open for more than this many hours (default 24).

## Usage

1. Create cold storage sites and transport trips with their temperature ranges.
2. Record temperature readings against a trip or a site.
3. Out-of-range readings automatically create or extend an open excursion with severity computed from the deviation.
4. A manager resolves each excursion with a note.
5. The daily cron flags excursions that stay open too long.

## Permissions

- `sf_cold_chain.group_sf_cold_chain_user` - sites, trips, readings and excursion tracking.
- `sf_cold_chain.group_sf_cold_chain_manager` - excursion resolution and trip cancellation.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.