# HANDOFF TEST — sf_lease_ifrs16

## 📍 Module Location
```
C:\Users\USER\Documents\Default Project\addons\sf_lease_ifrs16\
```

## 🎯 Priority Test Features (MUST HAVE)

| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | **PV Schedule** | Create lease (60 months, monthly, arrears, IBR 4.5%) → Activate → verify schedule: interest = opening × rate/12, principal = payment − interest, closing = opening − principal | 🔴 Critical |
| 2 | **Initial Measurement** | Verify liability = PV of payments; ROU = liability + direct costs + prepaid + restoration − incentives | 🔴 Critical |
| 3 | **Journal Entries** | "Post Due Entries" → verify move lines: Dr Interest, Dr Liability(principal), Dr Depreciation expense, Cr Acc. depreciation, Cr Bank; line.posted = True, move linked | 🔴 Critical |
| 4 | **Advance Timing** | Payment in advance: interest on balance after payment; PV exponents 0..n-1 | 🔴 Critical |
| 5 | **Modification** | Apply modification (new payment/term/IBR) → liability re-measured = new PV, ROU adjusted by delta, unposted lines rebuilt | 🔴 Critical |
| 6 | **Exemptions** | Check short-term or low-value → liability/ROU = 0, entries = straight-line expense + payment only | 🟡 High |
| 7 | **Multi-Company** | Company A lease invisible from Company B user | 🟡 High |
| 8 | **PDF Report** | Schedule PDF renders all periods + posted status | 🟢 Medium |
| 9 | **Lifecycle** | Close blocked until all periods posted; terminate → reopen draft works | 🟢 Medium |

## 🧪 Suggested Test Scenarios

### Scenario 1: Standard Lease Lifecycle (End-to-End)
```
1. Lease Contracts → New: "Office lease", lessor, start=today,
   36 months, monthly, arrears, payment 1000, IBR 12% (1%/month)
   → verify liability ≈ 36 × PV annuity factor ≈ 30,107.51
   → verify ROU = liability (+0 components)
2. Map accounts (Accounting tab): ROU, acc.dep., interest, dep.expense, journal
3. Activate Lease → 36 schedule lines generated
4. Check line 1: opening = 30,107.51; interest = 301.08;
   principal = 698.92; closing = 29,408.59
5. Post Due Entries → 1 move created & posted; line 1 marked posted
6. Print Schedule PDF → all 36 periods visible
7. After posting all 36 (simulate by backdating due dates): Close Lease works
```

### Scenario 2: Modification Mid-Term
```
1. Active lease from Scenario 1 with 2+ periods posted
2. Create Modification: new payment 1200, effective today, reason "index revision"
3. Apply → contract state = Modified; payment = 1200
4. Verify unposted lines rebuilt with new payment
5. Verify remeasured_liability = PV(remaining payments at IBR)
6. Verify adjustment = remeasured − liability before; chatter message posted
```

### Scenario 3: Exempt Lease
```
1. New lease: 10 months, payment 500, check "Short-term Exemption"
2. Verify liability = 0, ROU = 0, monthly_depreciation = 0
3. Activate → schedule with straight-line expense
4. Post Due Entries → move = Dr Lease expense 500 / Cr Bank 500 (no interest/principal)
```

### Scenario 4: Advance Payment Timing
```
1. New lease: 12 months, annual frequency, advance, payment 12,000, IBR 5%
2. Verify PV uses exponents 0..11 (not 1..12)
3. Verify period-1 interest computed on (opening − payment)
```

### Scenario 5: Multi-Company + Security
```
1. Two companies; create lease in Company A
2. User restricted to Company B → lease invisible
3. Lease User: cannot delete contract; Lease Manager: can
```

## ⚠️ Points à Surveiller (from auto-contrôle)

| Area | Issue | Impact | Mitigation |
|------|-------|--------|------------|
| **Liability account fallback** | `_liability_account()` uses system param or first current-liability account — may pick wrong account | High | Set `sf_lease_ifrs16.liability_account_id` system parameter before posting |
| **Advance timing interest** | Simplified formula (interest on balance after advance payment) | Medium | Compare against reference IFRS 16 calculator |
| **Modification depreciation** | New depreciation = (ROU + adjustment) / remaining total periods | Medium | Verify acceptable straight-line rebasing |
| **Rounding** | 2-decimal rounding per line; final line may drift ±0.05 | Low | Acceptable for v1; note in audit |
| **Demo data** | Uses `base.res_partner_2` and no account mapping | Low | Map accounts before activation in demo DB |

## 🔧 Test Instance Requirements

```bash
# Odoo 18.0 or 19.0 (Community or Enterprise)
# Depends auto-installed: base, account, mail
# Requires an accounting localization installed (for accounts/journals)
```

**Install:**
```bash
./odoo-bin -i sf_lease_ifrs16 -d test_db --load-language=en
```

## ✅ Acceptance Criteria (Module "Vendable")

| Criterion | Pass Condition |
|-----------|----------------|
| Install | Installs without error on clean Odoo 18/19 with accounting localization |
| PV math | Liability matches reference IFRS 16 calculator (±0.05) |
| ROU math | ROU = liability + IDC + prepaid + restoration − incentives |
| Schedule | N lines, interest/principal/closing coherent line to line |
| Entries | Posted move has 5 balanced lines (4 non-exempt) / 2 lines (exempt) |
| Modification | Liability re-measured, ROU adjusted, schedule rebuilt, chatter logged |
| Exemptions | Zero capitalization, straight-line expense entries |
| Multi-company | Record rules isolate data per company |
| PDF | Schedule report renders with all periods |
| No crashes | No tracebacks on all above flows |

## 📞 Contact
- **Support:** tech5262@gmail.com
- **Handoff Date:** 2026-08-23 (cycle 2)

---

> **Note:** Static quality control only (syntax, XML, security coverage, consistency). Functional testing on live Odoo instance NOT performed — that is this handoff's purpose.
