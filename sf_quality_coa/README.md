# sf_quality_coa — Certificate of Analysis (CoA)

Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow.

## Quick Install

```bash
cp -r sf_quality_coa /path/to/odoo/addons/
./odoo-bin -i sf_quality_coa -d your_database
```

## Dependencies

`base, stock, quality, mail`

## Workflow

- Create CoA per delivery (product/lot prefilled).
- Enter test results and verdicts.
- Tested -> Approved (all-pass gate) -> Issued.

## Features

- CoA per Delivery — Linked to the outgoing picking, product and lot.
- Test Parameters — Parameter, specification, measured result, unit, method.
- Pass/Fail Verdicts — All-pass gate before approval.
- Approval Workflow — Tested by technician, approved by manager, issued to customer.
- Dates — Production and expiry dates on the certificate.
- Multi-Company — Per-entity certificates.
- Audit Trail — Chatter with tester and approver.
- Role Groups — Technician and Approver.
- Standard Modules Only — base, stock, quality, mail.

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
