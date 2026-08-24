# sf_sample_management — Sample & Free Goods Management

Sample requests with approval, shipment, feedback and conversion tracking - full cost visibility on every sample.

## Quick Install

```bash
cp -r sf_sample_management /path/to/odoo/addons/
./odoo-bin -i sf_sample_management -d your_database
```

## Dependencies (auto-installed)

`base, sale_management, stock, product, mail`

## Workflow

- Log request (customer, purpose, lines with costs).
- Approve -> record shipment reference.
- Feedback -> link sale order -> Converted (won) or Lost.

## Features

- Sample Requests — Prospect/customer, purpose (evaluation, trade show, lab test, press), lines with quantities.
- Approval Workflow — Approve before shipping; costs computed from product cost plus shipping.
- Shipment Tracking — Tracking reference and delivery link.
- Feedback — Per-request feedback records with ratings and comments.
- Conversion Tracking — Link the resulting sale order: won/lost, cost per won deal visible.
- Multi-Company — Per-entity requests.
- Audit Trail — Chatter on requests and feedback.
- Role Groups — Sample User and Manager.
- Standard Modules Only — base, sale, stock, product, mail.

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
