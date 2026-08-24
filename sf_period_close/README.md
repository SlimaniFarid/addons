# sf_period_close — Month-End Close Checklist

Structured financial close: checklist templates, task orchestration, sign-offs, blockers and close calendar.

## Quick Install

```bash
cp -r sf_period_close /path/to/odoo/addons/
./odoo-bin -i sf_period_close -d your_database
```

## Dependencies (auto-installed)

`base, account, mail`

## Workflow

- Create checklist template (steps per department).
- Open Close Period: dates + template -> Generate Tasks.
- Work tasks to Done/NA, resolve blockers, Close.

## Features

- Reusable Templates — Steps per department with sequence and relative due days - define your close once.
- Close Periods — Generate the full task list per month with due dates computed automatically.
- Task Workflow — Pending, In Progress, Done, Blocked (with reason) and N/A - nothing falls through.
- Blocker Dashboard — See what stops the close and who owns it; period flags itself Blocked.
- Sign-offs — Per-task and final close sign-off with date and user.
- Progress % — Live completion percentage on every period.
- Multi-Company — Close calendar across entities with isolation.
- Audit Trail — Chatter on every task: state changes with timestamps.
- Standard Modules Only — base, account, mail.

## Compatibility

| Odoo Version | Status |
|--------------|--------|
| 18.0 | Primary target |
| 19.0 | Compatible |
| Editions | Community & Enterprise |
| Hosting | Odoo.sh, on-premise, Docker |

## License & Support

- **License:** OPL-1 — one-time purchase, lifetime usage
- **Support:** tech5262@gmail.com
- **Author:** Ethan Miller
- **Price:** €249 (one-time)
