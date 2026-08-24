# HANDOFF TEST — sf_bank_stmt_import_pro

## 📍 Module Location
```
C:\Users\USER\Documents\Default Project\addons\sf_bank_stmt_import_pro\
```

## 🎯 Priority Test Features (MUST HAVE)

| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | **MT940 parse** | Import a real bank MT940 file → lines parsed with correct sign (C/D), balances :60F/:62F → statement balance_start/balance_end_real | 🔴 Critical |
| 2 | **CAMT.053 parse** | Import a SEPA camt.053 XML → Ntry entries, DBIT negative, Bal OPBD/CLBD | 🔴 Critical |
| 3 | **CSV template** | Create template mapping a real bank CSV → parse → verify dates/amounts/reference per mapping, D/C marker flips sign | 🔴 Critical |
| 4 | **OFX / QIF parse** | Import OFX and QIF exports → transactions parsed | 🟡 High |
| 5 | **Duplicate detection** | Import same file twice → second run flags all lines duplicate, skipped; force-import option works | 🔴 Critical |
| 6 | **Statement creation** | Import Lines → account.bank.statement + lines created in correct journal, payment_ref filled, partner matched by exact name | 🔴 Critical |
| 7 | **Multi-currency** | Line with EUR code on USD journal → foreign_currency_id set (if EUR active) | 🟡 High |
| 8 | **Preview UX** | Parsed grid shows duplicates in red, stats (total/dup/net) correct, nothing imported before approval | 🟡 High |
| 9 | **Multi-company** | Run tied to journal company; user of company B cannot see it | 🟡 High |
| 10 | **Error handling** | Wrong format file → clear UserError message, no crash | 🟢 Medium |

## 🧪 Suggested Test Scenarios

### Scenario 1: MT940 German Bank (End-to-End)
```
1. Bank Import Pro > Templates > New: name "Deutsche Bank MT940",
   format MT940 (no mapping needed)
2. Import Runs > New: pick bank journal, template, upload .sta/.mt940 file
3. Parse File → preview shows transactions, balances read
4. Verify: credits positive, debits negative, reference from :86: ?20
5. Import Lines → statement opens; check balance_start/end_real
6. Re-parse same file in a new run → all lines flagged Duplicate
7. Import → 0 lines imported with clear message
```

### Scenario 2: Bank CSV with Template
```
1. Templates > New "MyBank CSV": delimiter ;, header 1 row,
   date col 0 (%d/%m/%Y), amount col 1, D/C col 2 (marker D),
   ref col 3, partner col 4, decimal , thousands .
2. Upload CSV: "02/08/2026;1.234,56;C;REF-1;ACME;Payment invoice 100"
3. Parse → amount = +1234.56, partner ACME matched if exists
4. Change D/C col value to D on a line file → amount negative
5. Import → statement lines created in journal
```

### Scenario 3: CAMT.053 SEPA
```
1. Download camt.053 XML from e-banking portal
2. Template format CAMT.053, upload, parse
3. Verify DBIT entries negative, CLBD balance on statement
4. Verify AcctSvcrRef used as reference
```

### Scenario 4: Dedup Edge Cases
```
1. Import file A (5 lines). Manually add a matching statement line
   in the journal (same date/amount/ref)
2. Re-run import of file A → that line also flagged duplicate
   (history detection works beyond module runs)
3. Uncheck "Skip Duplicates" → all lines import (force mode)
```

### Scenario 5: Security & Errors
```
1. Bank Import User: can create/parse/import; cannot delete template
2. Bank Import Manager: full CRUD
3. Upload an OFX file with an MT940 template → clear error message
4. Upload empty CSV → "No data rows could be parsed" error
5. Two companies: run in company A invisible from company B user
```

## ⚠️ Points à Surveiller (from auto-contrôle + parser tests)

| Area | Issue | Impact | Mitigation |
|------|-------|--------|------------|
| **Parsers validated offline** | 5 parsers tested on synthetic samples only (MT940/CAMT/OFX/QIF/CSV) — real bank files vary | High | Test with REAL files from your banks; edge layouts may need parser tweaks |
| **Dedup hash basis** | Uses payment_ref[:80]; banks with identical date+amount+ref same day = false duplicate | Medium | Force-import option; ref usually unique |
| **Partner matching** | Exact name only — no fuzzy | Low | Match at reconciliation |
| **balance_start on partial import** | If duplicates skipped, statement balances from file may not tie to imported lines | Medium | Review preview before import |
| **MT940 :86: variants** | Structured ?20-?33 tags vary by bank | Medium | Reference falls back to full communication |

## 🔧 Test Instance Requirements

```bash
# Odoo 18.0 or 19.0 (Community or Enterprise) with accounting localization
# Depends auto-installed: base, account, mail
# Prepare: 2+ bank journals, sample files (MT940, camt.053.xml, .ofx, .qif, .csv)
```

**Install:**
```bash
./odoo-bin -i sf_bank_stmt_import_pro -d test_db
```

## ✅ Acceptance Criteria (Module "Vendable")

| Criterion | Pass Condition |
|-----------|----------------|
| Install | Installs without error on clean Odoo 18/19 |
| MT940 | Real MT940 parses; signs, refs, balances correct |
| CAMT.053 | Real SEPA XML parses; DBIT negative; CLBD balance set |
| CSV | Template-driven parse matches manual verification |
| OFX/QIF | Standard exports parse without error |
| Dedup | Re-import flags duplicates; history detection works; force-import works |
| Import | Statement + lines in correct journal; partner matched; refs in label |
| Multi-currency | Foreign currency kept on line when applicable |
| Security | 2 groups enforce CRUD; company isolation works |
| Errors | Wrong/empty files give clear messages, no tracebacks |
| No crashes | All above flows without Python errors |

## 📞 Contact
- **Support:** tech5262@gmail.com
- **Handoff Date:** 2026-08-23 (cycle 3)

---

> **Note:** Static QC + offline parser validation done (synthetic samples for the 5 formats). Functional testing with REAL bank files on a live Odoo instance remains to be done by the test agent.
