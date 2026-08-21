# Freight Audit

Audit carrier invoices against your negotiated contracts and real shipments.
Detect overcharges, manage disputes, and recover the 3-10% of freight spend
that leaks away every year.

## Features
- Carrier contracts with rate grids, tolerances, allowed surcharges
- CSV invoice import with dry-run validation
- Automatic invoice-to-shipment matching (tracking reference)
- 6 verification rules: rate variance, unauthorized surcharge,
  weight/dim mismatch, duplicate billing, phantom shipment, VAT error
- Typed findings with severity thresholds per contract
- Dispute workflow with vendor credit note generation + reconciliation
- Payment blocked while disputes or findings are open
- Carrier compliance dashboard (pivot on variance by carrier/month)
- Multi-company, multi-currency, full chatter audit trail

## Installation
Copy to addons path, update apps list, install **Freight Audit**.

## Configuration
1. Settings > Users: assign *Freight Audit / User* or / Manager.
2. Create a contract per carrier with rate grid + allowed surcharges.
3. Import carrier invoices via Invoices > Import (dry-run report).

## Usage
1. Upload a monthly carrier invoice CSV; the wizard validates lines.
2. Click **Run Audit**: matching + rule engine produce typed findings.
3. Create a dispute from findings, submit, track carrier response.
4. Resolve by credit note: an `in_refund` is generated and reconciled.
5. Validate payment only when all findings are closed.

## Permissions
- `sf_freight_audit.group_sf_freight_audit_user` â€” read/write own company.
- `sf_freight_audit.group_sf_freight_audit_manager` â€” full access, all companies.

## Dependencies
base, mail, account, stock

## Compatibility
Odoo 18.0 and Odoo 19.0 (Community & Enterprise).
