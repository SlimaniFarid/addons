# sf_ic_netting — Intercompany Netting

Match open intercompany balances across entities, compute net positions per company pair and generate settlement entries.

## Quick Install

```bash
cp -r sf_ic_netting /path/to/odoo/addons/
./odoo-bin -i sf_ic_netting -d your_database
```

## Dependencies (auto-installed)

`base, account, mail`

## Workflow

- Create session: period + participating entities.
- Compute Positions -> net per company pair.
- Confirm, resolve disputes, Settle (posts net entries).

## Features

- One-Click Scan — All open receivable/payable items whose partner is another group company, matched via company partner records.
- Net per Pair — Receivables minus payables per company pair with open item counts and drill-down.
- Dispute Tracking — Flag individual items as disputed with reason and resolution notes before settling.
- Settlement Entries — Generate and post journal entries for net amounts (due to / due from).
- Multi-Company — Sessions scoped per owner entity; participants selected per session.
- Multi-Currency — Works across entities with different currencies via residual amounts.
- History — Every session keeps its positions, disputes and settlement moves.
- Audit Trail — Chatter records who computed, confirmed and settled.
- Standard Modules Only — base, account, mail. Nothing else.

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
