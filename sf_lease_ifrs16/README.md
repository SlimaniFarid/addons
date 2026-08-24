# sf_lease_ifrs16 — Lease Accounting (IFRS 16 / ASC 842)

Lessee-side lease capitalization native to Odoo Accounting: right-of-use assets,
lease liabilities, PV schedules, automated journal entries and modifications.

## Quick Install

```bash
# 1. Copy to your Odoo addons path
cp -r sf_lease_ifrs16 /path/to/odoo/addons/

# 2. Update Apps List (Settings -> Update Apps List)

# 3. Install
./odoo-bin -i sf_lease_ifrs16 -d your_database
```

## Dependencies (auto-installed)

| Module | Purpose |
|--------|---------|
| `base` | Core ORM, sequences, companies |
| `account` | Journal entries, accounts, journals |
| `mail` | Chatter, activities, notifications |

## Post-Install Configuration

### 1. User Groups (Settings -> Users & Companies -> Groups)

| Group | Typical User | Permissions |
|-------|--------------|-------------|
| **Lease Accounting User** | Accountant | Create/edit contracts, post due entries |
| **Lease Accounting Manager** | CFO / Controller | Full CRUD incl. delete, close leases |

### 2. Account Mapping (per contract, Accounting tab)

| Field | Typical Mapping |
|-------|-----------------|
| ROU Asset Account | Fixed assets -> Right-of-use assets |
| Accumulated Depreciation Account | Fixed assets -> Accumulated ROU depreciation |
| Interest Expense Account | Expenses -> Interest on lease liability |
| Depreciation Expense Account | Expenses -> ROU depreciation |
| Straight-line Expense Account (exempt) | Expenses -> Rent expense |
| Payment Journal | Company bank/cash journal |

### 3. Liability Account (global)

Set the system parameter `sf_lease_ifrs16.liability_account_id` to your
lease liability account (System Parameters), or ensure a current-liability
account exists as fallback.

## Workflow

```
1. Lease Accounting -> Lease Contracts -> New
2. Enter: lessor, dates, term, payment, frequency, timing, IBR
   + initial costs / incentives / prepaid / restoration
   -> Initial liability (PV) and ROU asset computed live
3. Map accounts (Accounting tab)
4. Click "Activate Lease" -> full PV amortization schedule generated
5. Monthly: click "Post Due Entries"
   -> interest + principal + depreciation + payment journal entries
6. Mid-contract change? Create a Modification
   -> remaining liability re-measured, ROU adjusted, schedule rebuilt
7. Audit: print the Schedule PDF (all periods + posted status)
```

## Accounting Logic (IFRS 16)

- **Initial liability** = Σ payment / (1 + r)^t, r = IBR / periods per year
- **Initial ROU** = liability + initial direct costs + prepaid rent
  + restoration costs − incentives
- **Period interest** = opening liability × r (effective interest method)
- **Principal** = payment − interest
- **ROU depreciation** = straight-line over lease term
- **Modification** = re-measure remaining PV at new terms; delta adjusts ROU

## Reports

| Report | Trigger | Output |
|--------|---------|--------|
| Lease Schedule PDF | "Schedule PDF" button | Full amortization table + posted status |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing accounting configuration" | Map all required accounts on the contract (Accounting tab) |
| Liability account not found | Set system parameter `sf_lease_ifrs16.liability_account_id` |
| Schedule empty | Click "Regenerate Schedule" or Activate the lease |
| Cannot close lease | All periods must be posted first |

## Compatibility

| Odoo Version | Status |
|--------------|--------|
| 18.0 | Primary target |
| 19.0 | Compatible (APIs stable) |
| Editions | Community & Enterprise |
| Hosting | Odoo.sh, on-premise, Docker |

## License & Support

- **License:** OPL-1 — one-time purchase, lifetime usage
- **Support:** tech5262@gmail.com
- **Author:** Ethan Miller
- **Price:** €349 (one-time)
