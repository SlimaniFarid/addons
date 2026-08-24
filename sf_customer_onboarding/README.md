# sf_customer_onboarding — Customer Onboarding Workflow

Structured customer onboarding: document checklist, setup tasks, progress tracking and first order.

## Quick Install

```bash
cp -r sf_customer_onboarding /path/to/odoo/addons/
./odoo-bin -i sf_customer_onboarding -d your_database
```

## Dependencies

`base, sale, mail`

## Workflow

- Build template steps.
- Start onboarding per customer (tasks generated).
- Complete tasks, then complete onboarding.

## Features

- Reusable Templates — Ordered steps: documents, contract, setup, training.
- One-Click Start — Generate the full task list per new customer.
- Task Completion — Toggle tasks done with dates and responsibles.
- Progress % — Live completion on every onboarding.
- First Order Link — Attach the resulting first sale order.
- Multi-Company — Per-entity onboardings.
- Audit Trail — Chatter on progress.
- Role Groups — Onboarding User and Manager.
- Standard Modules Only — base, sale, mail.

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
- **Price:** €199 (one-time)
