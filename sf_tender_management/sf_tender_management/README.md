# Tender Management & Sourcing (RFx)

Manage the full lifecycle of a tender / procurement consultation
(RFQ, RFI, RFP, public tender): published dossier, dated supplier
offers, weighted multi-criteria evaluation, automatic scoring,
justified award decision and audit archiving.

## Features

- Tender dossier with submission deadline and workflow
  (draft → published → in_evaluation → awarded → closed / cancelled)
- Dated offer deposits per supplier
- Weighted evaluation criteria and automatic weighted score
- Justified award decision with mandatory reason
- Deadline alerts via cron
- Evaluation summary report and dashboard

## Installation

Copy the module into your addons path, update the apps list and
install **Tender Management & Sourcing (RFx)**.

## Configuration

Settings → General Settings → Tender Management:

- **Tender deadline alert (days)**: number of days before a
  submission deadline when the buyer is alerted.

Create your tenders under **Tenders & Sourcing → Tenders**, define
evaluation criteria and record offers. Award the tender with a
justification once the evaluation is complete.

## Permissions

- **Tender Management User**: create dossiers and offers, view the
  tenders of their own company.
- **Tender Management Manager**: everything, including criteria,
  evaluation, award and multi-company access.

## Dependencies

- base
- mail
- contacts

## Compatibility

- Odoo 18.0 and 19.0
- Community and Enterprise