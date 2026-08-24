# sf_fx_hedging — FX Exposure & Hedging

Open FX position per currency from receivables/payables, forward contracts with settlement gain/loss tracking.

## Quick Install

```bash
cp -r sf_fx_hedging /path/to/odoo/addons/
./odoo-bin -i sf_fx_hedging -d your_database
```

## Dependencies (auto-installed)

`base, account, mail`

## Workflow

- Exposure Snapshots > Compute: net open FX per currency.
- Book forwards (direction, notional, strike, value date).
- Settle at maturity: spot-based gain/loss recorded.

## Features

- Exposure Snapshots — Net open position per currency from posted foreign-currency AR/AP items.
- Coverage Ratio — Hedged vs open exposure per currency, per direction.
- Forward Contracts — Buy/sell direction, notional, strike rate, value date, counterparty bank.
- Settlement P&L — At maturity: spot rate pulled from Odoo, realized gain/loss computed and stored.
- History — Snapshots and settled hedges kept for audit and analysis.
- Multi-Company — Per-entity exposures and hedges.
- Odoo Rates — Uses your currency rate table - one source of truth.
- Audit Trail — Chatter on snapshots and contracts.
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
- **Price:** €299 (one-time)
