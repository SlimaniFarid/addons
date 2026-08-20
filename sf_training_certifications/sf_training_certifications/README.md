Training & Certification Tracking
=================================

Centralize employee trainings and certifications with expiry
tracking, renewal alerts and a compliance matrix.

Features
--------

* Training catalog with categories and mandatory flags
* Session planning and registration management
* Certification issuance with expiration dates
* Expiry and renewal alerts (activities)
* Compliance matrix per employee / training
* Certification and compliance reports

Installation
------------

Install the module as usual: Apps > Training & Certification
Tracking > Install.

Usage
-----

1. Create trainings and categories (Training & Certifications >
   Trainings). Mark mandatory trainings as "Mandatory".
2. Create sessions, add registrations, then plan and mark the
   session done.
3. Issue certificates from a done session using the
   "Issue Certificates" wizard.
4. A daily cron flags certifications expiring within 30 days and
   creates an activity for the QHSE / training team.
5. Open the Compliance Matrix to review who is compliant on each
   mandatory training, and refresh it when needed.

Configuration
-------------

* The certification expiry alert window (default 30 days) can be
  changed on the company settings (Certification Expiry Alert).

Known Issues / Roadmap
----------------------

* eLearning / Slides link: version 2.
* Online assessment tests: version 2.

Technical
---------

* Version 18.0.1.0.0 / 19.0.1.0.0
* Depends: base, hr, mail
* License: OPL-1
* Author: Ethan Miller
* Support: tech5262@gmail.com