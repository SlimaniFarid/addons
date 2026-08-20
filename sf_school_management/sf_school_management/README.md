# School Management & Continuing Education (SIS)

Manage schools and training centres: students and records,
groups/classes, academic years, teachers, courses and enrollments,
absences with reason and justification, grades with coefficients and
weighted averages, PDF report cards, tuition fees with payments and
overdue alerts.

## Features

- Students and records (identity, birth date, tutors, status)
- Academic years and groups/classes with supervisors
- Teachers (linked to HR employees, optional)
- Courses and student/group enrollments
- Absences with reason and justification workflow
- Grades per student/course/period with coefficient and confirmed
  workflow (manager-only)
- Weighted average per student, subject averages and PDF report cards
- Tuition fees with amount due, paid status and overdue alerts (cron)
- Unpaid fees report (PDF)
- Dashboard of students by group and status
- Multi-company record rules and manager workflow

## Installation

Copy the module to your addons path, update the app list and install
**School Management & Continuing Education (SIS)**.

## Configuration

Assign the groups in Settings > Users:

- **School Management User**: register students, groups, courses,
  absences, grades and payments of their own company.
- **School Management Manager**: full access, grade confirmation,
  payment confirmation and multi-company access.

Company settings (Settings > School Management):
- **Overdue tuition alert (days)**: number of days after the due date
  before an overdue tuition fee triggers an alert.

## Usage

1. Create the academic year and the groups/classes.
2. Register teachers and students (an active student must belong to a
   group).
3. Create courses and enroll students.
4. Teachers enter grades; the manager confirms them.
5. Record absences and set them as justified or unjustified.
6. Create tuition fees and record payments; overdue fees raise
   activities via the daily cron.
7. Print the report card or the unpaid fees report.

## Permissions

- `sf_school_management.group_school_user` — read/write limited.
- `sf_school_management.group_school_manager` — full access, grade and
  payment confirmation, all companies.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts
- hr

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).