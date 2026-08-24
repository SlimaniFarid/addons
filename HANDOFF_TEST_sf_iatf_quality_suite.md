# HANDOFF TEST — sf_iatf_quality_suite

## 📍 Module Location
```
C:\Users\USER\Documents\Default Project\addons\sf_iatf_quality_suite\
```

## 🎯 Priority Test Features (from Cahier des Charges — MUST HAVE)

| # | Feature | Description | Priority |
|---|---------|-------------|----------|
| 1 | **FMEA (DFMEA & PFMEA)** | Create DFMEA + PFMEA linked, enter items, verify RPN = S×O×D, classes, actions, re-rating, revision | 🔴 Critical |
| 2 | **Control Plan Generation** | Generate CP from PFMEA (RPN threshold 150), activate → verify `quality.point` sync | 🔴 Critical |
| 3 | **APQP Phase Gates** | Create project, complete 23 elements, advance through 5 phases (gate = all Complete) | 🔴 Critical |
| 4 | **PPAP Package** | Level 3 submission, fill 18 elements, sign PSW, generate PDF package | 🔴 Critical |
| 5 | **MSA Gauge R&R** | Crossed study (3 parts × 3 operators × 2 trials), calculate → %GRR, ndc, conclusion | 🔴 Critical |
| 6 | **SPC Charts + Alerts** | X-bar/R n=5, 20 subgroups → limits, Cp/Cpk, Western Electric rules 1-4 alerts | 🔴 Critical |
| 7 | **Multi-Company Isolation** | 2 companies, user A sees only A's FMEAs, PPAP visible to customer via `customer_id` | 🟡 High |
| 8 | **Security Groups** | Quality User (CRUD own), Quality Manager (full+approve), PPAP Approver (sign PSW) | 🟡 High |
| 9 | **IoT Endpoint** | POST `/iatf/spc/ingest/<id>` → real-time WE rule check + alert creation | 🟢 Medium |
| 10 | **Reports** | Print FMEA, CP, APQP, PPAP, MSA, SPC → PDF output | 🟢 Medium |

## 🧪 Suggested Test Scenarios (Step-by-Step)

### Scenario 1: Complete Quality Project Lifecycle (End-to-End)
```
1. Create Process "Injection Molding" with operations + equipment
2. Create DFMEA for "Brake Pedal" → add 5 failure modes with S/O/D → verify RPN
3. Create PFMEA linked to Process → add 8 items → identify 3 high-RPN (>150)
4. Generate Control Plan from PFMEA (threshold 150) → 3 lines created
5. Activate Control Plan → verify 3 quality.points created in Quality app
6. Create APQP Project for same product → auto-loads 23 elements
7. Complete Phase 1 elements → advance to Phase 2 → ... → Phase 5 Complete
8. Create MSA Study for CP line #1 characteristic → Crossed, 3 parts, 3 ops, 2 trials
9. Enter measurements → Calculate → verify %GRR, ndc, conclusion
10. Create SPC Chart X-bar/R for same characteristic → enter 20 subgroups
11. Verify limits, Cp/Cpk calculated → trigger WE rule 1 (point > UCL) → alert created
12. Create PPAP Submission Level 3 → fill all 18 elements → sign PSW
13. Generate PPAP Package PDF → verify all elements + PSW included
```

### Scenario 2: Multi-Company Data Isolation
```
1. Create Company A (Supplier) and Company B (Customer)
2. Login as User A (Company A) → create FMEA, CP, PPAP
3. Login as User B (Company B) → verify FMEA/CP NOT visible
4. On PPAP Submission from Company A, set customer_id = Company B
5. Login as User B → verify PPAP visible (customer_id rule)
6. Login as User A → verify all records visible
```

### Scenario 3: Security Group Permissions
```
1. Create users: inspector (Quality User), engineer (Quality Engineer), 
   manager (Quality Manager), approver (PPAP Approver)
2. Inspector: can create/read/write own FMEA, cannot approve, cannot unlink
3. Engineer: full CRUD on all, can approve FMEA/CP, cannot unlink
4. Manager: full + unlink, can approve everything
5. Approver: can read/write PPAP state, can sign PSW, cannot edit FMEA
```

### Scenario 4: IoT Real-Time SPC
```
1. Create SPC Chart X-bar/R, enable iot_enabled=True, set iot_topic="spc/chart/1"
2. POST to /iatf/spc/ingest/<chart_id> with {"value": 100.5, "subgroup_index": 1}
3. Verify measurement created, subgroup mean calculated
4. POST 5 points all > UCL → verify WE Rule 1 alert created (New state)
5. Acknowledge alert → state changes to Acknowledged
```

### Scenario 5: Revision & Traceability
```
1. Active FMEA → "New Revision" → new draft created with revision+1
2. Verify original stays Active, new is Draft
3. PFMEA item with high RPN → generate CP line → verify fmea_item_id link
4. CP line → quality_point_id created on activation
5. PPAP element 4 (DFMEA) → linked_dfmea_id traceability
6. APQP element 6 (DFMEA) → linked_dfmea_id same record
```

## ⚠️ Points à Surveiller (from Auto-Contrôle Étape 4)

| Area | Issue | Impact | Mitigation |
|------|-------|--------|------------|
| **SPC Attribute Charts** | p, np, c, u charts — limit calculations are placeholders | Medium | Test only variable charts (X-bar/R, X-bar/S, I-MR) for v1 |
| **MSA Nested/Attribute** | `_calculate_nested_grr()`, `_calculate_attribute()` are stubs | Low | Only Crossed (ANOVA) is fully implemented |
| **PPAP PDF Generator** | Calls `action_report_ppap_package` — QWeb report template needed | High | Template missing — PDF generation will fail |
| **IoT Controller** | Model has `ingest_iot_measurement()` but no HTTP controller route | Medium | Route `/iatf/spc/ingest/<id>` not implemented |
| **Demo Data** | `iatf_demo.xml` empty — requires pre-existing products/users/equipment | Low | Test agent must create master data first |

## 🔧 Test Instance Requirements

```bash
# Odoo 18.0 or 19.0 (Community or Enterprise)
# Required modules (auto-installed via depends):
#   base, quality, maintenance, mrp, stock, mail, product

# PostgreSQL 13+
# Python 3.10+
# wkhtmltopdf for PDF reports
```

**Install Command:**
```bash
./odoo-bin -i sf_iatf_quality_suite -d test_db --db_host=localhost --db_user=odoo --db_password=odoo
```

## ✅ Acceptance Criteria (Module "Vendable")

| Criterion | Pass Condition |
|-----------|----------------|
| **Install** | Module installs without error on clean Odoo 18.0/19.0 |
| **FMEA Core** | Create DFMEA+PFMEA, RPN auto-calculates, actions track, revision works |
| **CP ↔ FMEA** | Generate CP from PFMEA (RPN threshold), lines created, sync to quality.point on activate |
| **APQP Gates** | 23 elements loaded, phase gate blocks advance if incomplete, Gantt renders |
| **PPAP Package** | Level 3 submission, all 18 elements fillable, PSW auto-fills, PDF generates (when QWeb added) |
| **MSA Crossed** | 3×3×2 study calculates %GRR, ndc, Cp/Cpk, conclusion matches AIAG criteria |
| **SPC Variable** | X-bar/R limits calc, Cp/Cpk, WE Rules 1-4 trigger alerts with workflow |
| **Multi-Company** | Company A user sees only A's data; PPAP visible to customer company |
| **Security** | 5 groups enforce correct permissions (matrix in Scenario 3) |
| **No Crashes** | No Python tracebacks, no XML parse errors, no missing field errors |
| **Performance** | <2s for typical operations (create FMEA, calculate MSA, render SPC chart) |

## 📞 Contact
- **Developer:** Ethan Miller (this factory cycle)
- **Support Email:** tech5262@gmail.com
- **Handoff Date:** 2024-08-23

---

> **Note:** This module has passed **static quality control only** (syntax, XML validity, model-view consistency, security coverage, catalog uniqueness). **Functional testing on live Odoo instance has NOT been performed** — that is the purpose of this handoff.