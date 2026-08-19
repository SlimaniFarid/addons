Energy & Utility Consumption Monitoring
========================================

Track electricity, gas and water consumption per site and meter,
with cost allocation and reduction targets.

Features
--------

* Sites and meters modeling (electricity, gas, water)
* Periodic reading entry with confirmation workflow
* Automatic consumption and cost calculation
* Reduction targets with breach alerts
* Dashboard and ESG reports
* CSV reading import

Installation
------------

Install the module as usual: Apps > Energy & Utility Consumption
Monitoring > Install.

Usage
-----

1. Create your sites (Energy Monitoring > Sites).
2. Create meters per site and set the unit price (Energy
   Monitoring > Meters).
3. Enter periodic readings (Energy Monitoring > Readings); confirm
   readings after validation.
4. Define reduction targets (Energy Monitoring > Objectives).
   A daily cron checks objectives and schedules an activity when a
   target is breached.
5. Review consumption in the dashboard and reports.

Configuration
-------------

* Meter unit price (price_unit) drives the estimated cost of each
  reading.
* Objectives are checked daily by an automated action.

Known Issues / Roadmap
----------------------

* Connected meters / IoT API: version 2.
* Complete carbon footprint (scopes 1-2-3): version 2.

Technical
---------

* Version 18.0.1.0.0 / 19.0.1.0.0
* Depends: base, mail
* License: OPL-1
* Author: Ethan Miller
* Support: tech5262@gmail.com