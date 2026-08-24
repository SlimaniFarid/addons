# sf_iatf_quality_suite — IATF 16949 Automotive Quality Toolkit

Complete AIAG-VDA automotive quality management toolchain native to Odoo 18/19 Manufacturing & Quality.

## Quick Install

```bash
# 1. Copy to your Odoo addons path
cp -r sf_iatf_quality_suite /path/to/odoo/addons/

# 2. Update Apps List (Settings → Update Apps List)

# 3. Install
./odoo-bin -i sf_iatf_quality_suite -d your_database
# Or via Apps menu: search "IATF 16949" → Install
```

## Dependencies (auto-installed)

| Module | Odoo App | Purpose |
|--------|----------|---------|
| `base` | Base | Core ORM, sequences, companies |
| `quality` | Quality | `quality.point`, `quality.check` integration |
| `maintenance` | Maintenance | Equipment for MSA/SPC linkage |
| `mrp` | Manufacturing | `mrp.production`, `mrp.workcenter` linkage |
| `stock` | Inventory | `stock.lot`, `stock.picking` traceability |
| `mail` | Discuss | Chatter, activities, notifications |
| `product` | Products | `product.product`, `product.template` |

## Post-Install Configuration

### 1. User Groups (Settings → Users & Companies → Groups)

| Group | Implied By | Typical User | Permissions |
|-------|------------|--------------|-------------|
| **IATF Quality User** | Quality / User | Inspector, operator | Read/Create/Write own records |
| **IATF Quality Engineer** | Quality User | Quality engineer | Full CRUD on all quality records |
| **IATF Quality Manager** | Quality Engineer | Quality manager | Full + approve/validate + unlink |
| **IATF APQP Project Lead** | Quality Engineer | APQP project lead | CRUD APQP projects/elements |
| **IATF PPAP Approver** | Quality Engineer | Customer/supplier quality | Read/Write PPAP state, sign PSW |

> **Assign groups** to users based on role. Quality Manager gets full access including multi-company.

### 2. Multi-Company Setup (if applicable)

- Record rules (`ir.rule`) enforce data isolation per company automatically
- PPAP submissions are visible to both supplier and customer companies via `customer_id`
- Configure companies under Settings → Companies before creating quality records

### 3. Sequences (auto-created)

| Sequence | Prefix | Used By |
|----------|--------|---------|
| `iatf.fmea.dfmea` | DFMEA- | Design FMEA |
| `iatf.fmea.pfmea` | PFMEA- | Process FMEA |
| `iatf.control.plan` | CP- | Control Plan |
| `iatf.apqp.project` | APQP- | APQP Project |
| `iatf.ppap.submission` | PPAP- | PPAP Submission |
| `iatf.msa.study` | MSA- | MSA Study |
| `iatf.spc.chart` | SPC- | SPC Chart |

### 4. Integration Points

| Odoo Model | Linked From | Purpose |
|------------|-------------|---------|
| `quality.point` | Control Plan lines | Auto-created when CP activated |
| `maintenance.equipment` | MSA Study, SPC Chart | Measurement device linkage |
| `mrp.production` | FMEA, CP, PPAP | Link quality docs to production orders |
| `stock.lot` | PPAP sample parts | Traceability from PPAP to production |
| `res.partner` | Customer/supplier | Quality roles on PPAP, APQP |

## Typical Workflow

```
1. Create Process(es) with operations & equipment
   → Manufacturing → Configuration → Processes

2. Create DFMEA for product design
   → IATF 16949 Toolkit → FMEA → New (Type: DFMEA)

3. Create PFMEA for manufacturing process
   → Link to Process → Identify high-RPN items

4. Generate Control Plan from PFMEA
   → Control Plans → New → "Generate from PFMEA" button
   → Set RPN threshold (default 150) → Activate → Syncs to Quality Points

5. Run APQP Project through 5 phases
   → APQP Projects → New → Auto-loads 23 elements
   → Complete elements → Phase gate → Advance

6. Execute MSA Studies for critical characteristics
   → MSA Studies → New → Crossed/Nested/Attribute
   → Enter measurements → Calculate → Links to CP line

7. Monitor production with SPC Charts
   → SPC Charts → New → Select chart type
   → Enter subgroup data → Auto-limits, Cp/Cpk, alerts
   → Enable IoT for real-time sensor ingestion

8. Compile PPAP Package for customer submission
   → PPAP Submissions → New → Level 3 (default)
   → Fill 18 elements → Sign PSW → Generate PDF Package
```

## IoT / Real-Time SPC (Optional)

Enable on SPC Chart: `iot_enabled = True`, set `iot_topic`.

POST measurements to:
```
POST /iatf/spc/ingest/<chart_id>
Content-Type: application/json

{
  "value": 12.345,
  "subgroup_index": 1,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Triggers automatic Western Electric rule checking and alert creation.

## Reports (QWeb PDF)

| Report | Trigger | Output |
|--------|---------|--------|
| FMEA Report | Print from FMEA form | AIAG-VDA format with RPN history |
| Control Plan | Print from CP form | AIAG 3-phase format |
| APQP Status | Print from APQP form | Phase gate completion |
| PPAP Package | "Generate Package" button | Single PDF: cover + TOC + 18 elements + PSW |
| MSA Report | Print from MSA form | ANOVA table, %GRR, ndc, capability |
| SPC Chart | Print from SPC form | Control chart + limits + capability indices |

## Upgrading

```bash
# Pull latest code
cd /path/to/odoo/addons/sf_iatf_quality_suite
git pull

# Upgrade module
./odoo-bin -u sf_iatf_quality_suite -d your_database
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not appearing in Apps | Settings → Update Apps List → search "IATF" |
| Quality Points not created | Control Plan must be in "Active" state; check `active_sync` on lines |
| MSA calculation errors | Ensure ≥2 parts, ≥2 operators, ≥2 trials; check equipment calibration date |
| SPC limits not calculating | Need ≥20 subgroup points for X-bar/R; check `subgroup_size` matches data |
| Multi-company access denied | Verify user has correct company in allowed companies; check `ir.rule` domain |

## License & Support

- **License:** OPL-1 (Odoo Proprietary License v1.0) — one-time purchase, lifetime usage, source code included
- **Support:** tech5262@gmail.com
- **Author:** Ethan Miller
- **Price:** €449 (one-time, lifetime)

## Compatibility

| Odoo Version | Status |
|--------------|--------|
| 18.0 | ✅ Primary target, fully tested |
| 19.0 | ✅ Compatible (APIs stable) |
| Editions | Community & Enterprise |
| Hosting | Odoo.sh, On-premise, Docker (not Odoo Online) |

## Version History

See [CHANGELOG.md](CHANGELOG.md)