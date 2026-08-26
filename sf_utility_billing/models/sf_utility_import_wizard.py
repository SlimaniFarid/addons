# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityImportWizard(models.TransientModel):
    _name = 'sf.utility.import.wizard'
    _description = 'Import Utility Meter Readings'

    campaign_id = fields.Many2one('sf.utility.campaign', string='Campaign', required=True)
    meter_id = fields.Many2one('sf.utility.meter', string='Meter')
    data = fields.Text(
        string='Data',
        required=True,
        help='One reading per line.\n'
             'If a meter is selected: index[,YYYY-MM-DD]\n'
             'Otherwise: meter,index[,YYYY-MM-DD] where meter is the name, '
             'serial or id.\nThe date defaults to the campaign period end.',
    )

    def _parse_date(self, value, line_no):
        if not value:
            return self.campaign_id.period_end
        try:
            return fields.Date.from_string(value.strip())
        except (TypeError, ValueError):
            raise UserError(_('Line %s: invalid date "%s". Use YYYY-MM-DD.') % (line_no, value))

    def _parse_float(self, value, line_no, label):
        try:
            return float(value)
        except (TypeError, ValueError):
            raise UserError(_('Line %s: invalid %s "%s".') % (line_no, label, value))

    def _find_meter(self, value, line_no):
        meter = self.env['sf.utility.meter']
        try:
            meter = meter.browse(int(value))
        except (TypeError, ValueError):
            pass
        if not meter.exists():
            meter = self.env['sf.utility.meter'].search([('name', '=', value)], limit=1)
        if not meter:
            meter = self.env['sf.utility.meter'].search([('serial', '=', value)], limit=1)
        if not meter:
            raise UserError(_('Line %s: meter "%s" not found.') % (line_no, value))
        return meter

    def action_import(self):
        self.ensure_one()
        if self.campaign_id.state != 'open':
            raise UserError(_('Readings can only be imported into an open campaign.'))
        lines = [l for l in (self.data or '').splitlines() if l.strip()]
        if not lines:
            raise UserError(_('No data to import.'))
        errors = []
        rows = []
        for line_no, raw in enumerate(lines, start=1):
            parts = [p.strip() for p in raw.split(',')]
            try:
                if self.meter_id:
                    if len(parts) not in (1, 2):
                        raise UserError(_('Line %s: expected "index[,date]".') % line_no)
                    meter = self.meter_id
                    index = self._parse_float(parts[0], line_no, 'index')
                    date = self._parse_date(parts[1] if len(parts) == 2 else '', line_no)
                else:
                    if len(parts) not in (2, 3):
                        raise UserError(_('Line %s: expected "meter,index[,date]".') % line_no)
                    meter = self._find_meter(parts[0], line_no)
                    index = self._parse_float(parts[1], line_no, 'index')
                    date = self._parse_date(parts[2] if len(parts) == 3 else '', line_no)
                if meter.id not in self.campaign_id.meter_ids.ids:
                    raise UserError(_(
                        'Line %s: meter %s is not part of the campaign.') % (line_no, meter.name))
                rows.append((meter, index, date))
            except UserError as e:
                errors.append(str(e))
        if errors:
            raise UserError('\n'.join(errors))
        created = 0
        updated = 0
        skipped = 0
        for meter, index, date in rows:
            existing = self.campaign_id.reading_ids.filtered(
                lambda r: r.meter_id.id == meter.id)[:1]
            if existing:
                if existing.state == 'validated':
                    skipped += 1
                    continue
                existing.write({'index': index, 'reading_date': date})
                updated += 1
            else:
                self.env['sf.utility.meter.reading'].create({
                    'meter_id': meter.id,
                    'campaign_id': self.campaign_id.id,
                    'reading_date': date,
                    'index': index,
                    'company_id': meter.company_id.id,
                })
                created += 1
        message = _('%s reading(s) created, %s updated.') % (created, updated)
        if skipped:
            message += _(' %s validated reading(s) skipped.') % skipped
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'title': _('Import completed'),
            'message': message,
            'sticky': False,
        }