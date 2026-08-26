# -*- coding: utf-8 -*-
import csv
import io
from datetime import datetime, timedelta

from odoo import _, fields, models
from odoo.exceptions import UserError

EXPECTED_COLUMNS = [
    'invoice_ref', 'tracking_ref', 'charge_type', 'description',
    'ship_date', 'weight_kg', 'amount_billed',
]

CHARGE_MAP = {
    'base_freight': 'base_freight',
    'fuel_surcharge': 'fuel_surcharge',
    'security': 'security',
    'residential': 'residential',
    'liftgate': 'liftgate',
    'insurance': 'insurance',
    'customs': 'customs',
    'accessorial_other': 'accessorial_other',
    'other': 'other',
}


class SfFreightImportWizard(models.TransientModel):
    _name = 'sf.freight.import.wizard'
    _description = 'Import Freight Carrier Invoice (CSV)'

    carrier_id = fields.Many2one('res.partner', string='Carrier',
                                 required=True,
                                 domain=[('is_company', '=', True)])
    contract_id = fields.Many2one('sf.freight.carrier.contract',
                                  string='Contract',
                                  domain="[('partner_id', '=', carrier_id),"
                                         " ('state', '=', 'active')]")
    invoice_ref = fields.Char(string='Carrier Invoice Number',
                              required=True)
    invoice_date = fields.Date(string='Invoice Date',
                               default=fields.Date.today)
    csv_file = fields.Binary(string='CSV File', required=True)
    csv_filename = fields.Char()
    dry_run = fields.Boolean(string='Dry Run (validate only)',
                             default=True)

    def action_import(self):
        self.ensure_one()
        if not self.csv_file:
            raise UserError(_('Please upload a CSV file.'))
        import base64
        raw = base64.b64decode(self.csv_file)
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = raw.decode('latin-1')
        reader = csv.DictReader(io.StringIO(text))
        headers = reader.fieldnames or []
        missing = [c for c in EXPECTED_COLUMNS if c not in headers]
        if missing:
            raise UserError(_(
                'Missing CSV columns: %s') % ', '.join(missing))

        ok_lines, rejected = [], []
        for idx, row in enumerate(reader, start=2):
            err = self._validate_row(row)
            if err:
                rejected.append({'row': idx, 'error': err})
                continue
            ok_lines.append(row)

        if self.dry_run:
            message = _(
                'Dry run: %(ok)d valid lines, %(ko)d rejected.\n'
                '%(detail)s'
            ) % {
                'ok': len(ok_lines),
                'ko': len(rejected),
                'detail': '\n'.join(
                    _('Row %(r)s: %(e)s') % d for d in rejected[:20]),
            }
            return {'type': 'ir.actions.act_window',
                    'name': _('Dry Run Result'),
                    'res_model': 'sf.freight.import.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_dry_run_message': message}}

        if not ok_lines:
            raise UserError(_('No valid line found in the file.'))

        invoice = self.env['sf.freight.invoice'].create({
            'carrier_id': self.carrier_id.id,
            'contract_id': self.contract_id.id,
            'invoice_ref': self.invoice_ref,
            'invoice_date': self.invoice_date,
            'source': 'csv',
            'state': 'imported',
            'line_ids': [(0, 0, self._prepare_line(row))
                         for row in ok_lines],
        })
        invoice.action_run_audit()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Imported Invoice'),
            'res_model': 'sf.freight.invoice',
            'res_id': invoice.id,
            'view_mode': 'list,form',
        }

    def _validate_row(self, row):
        if not row.get('invoice_ref'):
            return _('Missing invoice_ref')
        if not row.get('amount_billed'):
            return _('Missing amount_billed')
        try:
            float(row.get('amount_billed', 0))
        except (ValueError, TypeError):
            return _('Invalid amount_billed')
        charge = CHARGE_MAP.get((row.get('charge_type') or '').strip())
        if not charge:
            return _('Unknown charge_type: %s')
        if row.get('ship_date'):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    datetime.strptime(row['ship_date'], fmt)
                    break
                except ValueError:
                    continue
            else:
                return _('Invalid ship_date format')
        return None

    def _prepare_line(self, row):
        ship_date = False
        if row.get('ship_date'):
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    ship_date = datetime.strptime(
                        row['ship_date'], fmt).date()
                    break
                except ValueError:
                    continue
        return {
            'description': row.get('description') or '',
            'charge_type': CHARGE_MAP[row['charge_type'].strip()],
            'tracking_ref': (row.get('tracking_ref') or '').strip(),
            'ship_date': ship_date,
            'uom_weight': float(row.get('weight_kg') or 0),
            'amount_billed': float(row['amount_billed']),
        }
