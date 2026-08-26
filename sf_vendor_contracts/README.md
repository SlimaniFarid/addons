Supplier Contract & Agreement Manager
======================================

Centralize your supplier contracts with clauses, amounts,
expiration dates and automatic renewal alerts.

Features
--------

* Supplier contract register
* Contract types, amounts and currencies
* Clauses and product lines
* Expiration and renewal alerts (activities)
* Contract versions and renewal history
* Expiring contracts report
* Contract register report

Installation
------------

Install the module as usual: Apps > Supplier Contract &
Agreement Manager > Install.

Usage
-----

1. Create a contract (Vendor Contracts > Contracts) with the
   supplier, dates, amount and clauses.
2. Activate it. A first version is recorded automatically.
3. A daily cron flags contracts expiring within the renewal
   notice window (default 60 days) and creates an activity for
   the buyer.
4. Use "Renew" to create the next version, or "Cancel" to close
   the contract.

Configuration
-------------

* The renewal notice window (default 60 days) can be changed on
  the company settings (Contract Expiry Alert).

Known Issues / Roadmap
----------------------

* Electronic signature: version 2.
* Link purchase orders to contracts: version 2.

Technical
---------

* Version 18.0.1.0.0 / 19.0.1.0.0
* Depends: base, product, mail
* License: OPL-1
* Author: Ethan Miller
* Support: tech5262@gmail.com