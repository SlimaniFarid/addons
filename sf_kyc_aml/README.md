# sf_kyc_aml — KYC / AML Due Diligence

Customer due diligence register: risk rating, screening cycles, UBO declaration and periodic reviews.

## Quick Install

```bash
cp -r sf_kyc_aml /path/to/odoo/addons/
./odoo-bin -i sf_kyc_aml -d your_database
```

## Dependencies

`base, mail`

## Workflow

- Create KYC file per partner.
- Complete document checklist and screening.
- Approve; next review computed from cycle.

## Features

- KYC Files — One file per partner with risk rating and status workflow.
- PEP / Sanctions Screening — Record screening date and result per file.
- UBO Declaration — Track ultimate beneficial owner declarations.
- Document Checklist — ID document, proof of address, bank details verification.
- Review Cycles — Configurable review frequency with next review computed and overdue flags.
- Expiry Workflow — Approved files expire and require re-approval.
- Multi-Company — Per-entity registers.
- Audit Trail — Chatter with every state change.
- Standard Modules Only — base, mail.

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
- **Price:** €299 (one-time)
