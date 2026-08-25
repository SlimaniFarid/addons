# -*- coding: utf-8 -*-
"""Per-bank CSV import templates."""
from odoo import api, fields, models, _


class SfBankStmtTemplate(models.Model):
    """Saved column mapping and formatting options for one bank layout."""
    _name = 'sf.bank.stmt.template'
    _description = 'Bank Statement Import Template'
    _order = 'name'

    name = fields.Char(string='Template Name', required=True)
    bank_id = fields.Many2one('res.bank', string='Bank')
    file_format = fields.Selection([
        ('mt940', 'MT940 (SWIFT)'),
        ('camt053', 'CAMT.053 (ISO 20022)'),
        ('ofx', 'OFX'),
        ('qif', 'QIF'),
        ('csv', 'CSV / Excel export'),
    ], string='File Format', required=True, default='csv')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    # CSV mapping
    csv_delimiter = fields.Selection([
        (',', 'Comma ,'),
        (';', 'Semicolon ;'),
        ('\t', 'Tab'),
        ('|', 'Pipe |'),
    ], string='CSV Delimiter', default=';')
    csv_encoding = fields.Selection([
        ('utf-8', 'UTF-8'),
        ('utf-8-sig', 'UTF-8 with BOM'),
        ('latin-1', 'Latin-1 / ANSI'),
        ('cp1252', 'Windows-1252'),
    ], string='File Encoding', default='utf-8-sig')
    csv_header_row = fields.Integer(string='Header Rows to Skip', default=1)
    date_col = fields.Integer(string='Date Column (0-based)')
    value_date_col = fields.Integer(string='Value Date Column (0-based, optional)')
    amount_col = fields.Integer(string='Amount Column (0-based)')
    debit_credit_col = fields.Integer(
        string='Debit/Credit Column (0-based, optional)',
        help='When amounts are unsigned: column containing D/C or '
             'debit/credit marker.')
    debit_value = fields.Char(string='Debit Marker', default='D',
                              help='Value meaning money out (debit).')
    reference_col = fields.Integer(string='Reference Column (0-based, optional)')
    partner_col = fields.Integer(string='Partner Name Column (0-based, optional)')
    communication_col = fields.Integer(
        string='Communication Column (0-based, optional)')
    currency_col = fields.Integer(
        string='Currency Column (0-based, optional)')
    date_format = fields.Selection([
        ('%Y-%m-%d', '2026-08-23 (ISO)'),
        ('%d/%m/%Y', '23/08/2026'),
        ('%d.%m.%Y', '23.08.2026'),
        ('%m/%d/%Y', '08/23/2026'),
        ('%d-%m-%Y', '23-08-2026'),
        ('%Y%m%d', '20260823'),
    ], string='Date Format', default='%d/%m/%Y')
    decimal_separator = fields.Selection([
        ('.', 'Dot . (1,234.56)'),
        (',', 'Comma , (1.234,56)'),
    ], string='Decimal Separator', default=',')
    thousands_separator = fields.Selection([
        (',', 'Comma ,'),
        ('.', 'Dot .'),
        ('', 'None'),
    ], string='Thousands Separator', default='.')
