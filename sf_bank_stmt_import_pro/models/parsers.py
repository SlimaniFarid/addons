# -*- coding: utf-8 -*-
from odoo import fields
"""Pure-python parsers: MT940, CAMT.053, OFX, QIF. No third-party deps."""
import re
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO

import csv as csv_module
from datetime import datetime


class ParseError(Exception):
    pass


def _to_float(text, decimal=',', thousands='.'):
    if text is None:
        return 0.0
    cleaned = str(text).strip().replace(thousands, '')
    if decimal == ',':
        cleaned = cleaned.replace(',', '.')
    cleaned = re.sub(r'[^0-9.\-]', '', cleaned)
    return float(cleaned) if cleaned not in ('', '-') else 0.0


def _parse_date(text, fmt='%d/%m/%Y'):
    text = str(text).strip()
    for candidate_fmt in (fmt, '%Y-%m-%d', '%d/%m/%Y', '%d.%m.%Y', '%Y%m%d'):
        try:
            return datetime.strptime(text, candidate_fmt).date()
        except ValueError:
            continue
    raise ParseError('Unreadable date: %s' % text)


# ----------------------------------------------------------------------
# MT940
# ----------------------------------------------------------------------
_TAG_RE = re.compile(r'(:\d{2}[A-Z]??:)')


def parse_mt940(raw_bytes, **kwargs):
    """Parse SWIFT MT940; returns dict with lines, balance_start, balance_end."""
    text = raw_bytes.decode('latin-1', errors='replace')
    text = text.replace('-}', '').replace('\r\n', '\n').replace('\r', '\n')

    # Re-join continuation lines (no leading tag or dash)
    raw_lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if _TAG_RE.match(line) or line.startswith(':'):
            raw_lines.append(line)
        elif raw_lines:
            raw_lines[-1] += line

    lines = []
    balance_start = balance_end = 0.0
    currency = False
    current = None

    def close_current():
        nonlocal current
        if current and current.get('date') and 'amount' in current:
            lines.append(current)
        current = None

    for line in raw_lines:
        m = re.match(r':(\d{2}[A-Z]?):(.*)', line)
        if not m:
            continue
        tag, content = m.group(1), m.group(2).strip()
        if tag == '25':
            currency = currency or False
        elif tag in ('60F', '60M'):
            close_current()
            # D/C mark, YYMMDD, currency, amount
            m2 = re.match(r'([CD])(\d{6})([A-Z]{3})?([\d,\.]+)', content)
            if m2:
                balance_start = _to_float(m2.group(4))
                if m2.group(1) == 'D':
                    balance_start = -balance_start
                if m2.group(3):
                    currency = m2.group(3)
        elif tag == '61':
            close_current()
            m2 = re.match(
                r'(\d{6})(\d{4})?(?:\d{2}[A-Z])?([CD])(?:[A-Z]{3})?'
                r'N?([\d,\.]+)', content)
            if m2:
                d = datetime.strptime(m2.group(1)[:6], '%y%m%d').date()
                sign = -1.0 if m2.group(3) == 'D' else 1.0
                current = {
                    'date': d,
                    'amount': sign * _to_float(m2.group(4)),
                    'reference': '',
                    'communication': '',
                }
        elif tag == '86' and current:
            parts = re.split(r'\?(\d{2})', content)
            comm = ''
            for i in range(1, len(parts), 2):
                comm += parts[i + 1] if i + 1 < len(parts) else ''
            comm = ' '.join(comm.split())
            current['communication'] = comm
            ref_m = re.search(r'REF[.:\s]?([A-Z0-9\-\/]+)', comm, re.I)
            current['reference'] = ref_m.group(1) if ref_m else comm[:60]
        elif tag in ('62F', '62M'):
            close_current()
            m2 = re.match(r'([CD])(\d{6})([A-Z]{3})?([\d,\.]+)', content)
            if m2:
                balance_end = _to_float(m2.group(4))
                if m2.group(1) == 'D':
                    balance_end = -balance_end
    close_current()
    if not lines:
        raise ParseError('No :61: transaction lines found in MT940 file.')
    return {'lines': lines, 'balance_start': balance_start,
            'balance_end': balance_end, 'currency': currency}


# ----------------------------------------------------------------------
# CAMT.053
# ----------------------------------------------------------------------
def _camt_local(tag):
    return './/{*}' + tag


def parse_camt053(raw_bytes, **kwargs):
    """Parse ISO 20022 CAMT.053 XML; namespace-agnostic."""
    try:
        root = ET.fromstring(raw_bytes)
    except ET.ParseError as exc:
        raise ParseError('Invalid XML: %s' % exc)

    lines = []
    balance_start = balance_end = 0.0
    currency = False

    bal_nodes = root.findall('.//{*}Bal')
    for bal in bal_nodes:
        type_node = bal.find('.//{*}Tp/{*}CdOrPrtry/{*}Cd')
        amount_node = bal.find('.//{*}Amt')
        credit = bal.find('.//{*}CdtDbtInd')
        if amount_node is None:
            continue
        amount = _to_float(amount_node.text, '.', ',')
        if credit is not None and credit.text == 'DBIT':
            amount = -amount
        code = type_node.text if type_node is not None else ''
        if code == 'OPBD':
            balance_start = amount
        elif code == 'CLBD':
            balance_end = amount
        if amount_node.get('Ccy') and not currency:
            currency = amount_node.get('Ccy')

    for entry in root.findall('.//{*}Ntry'):
        amount_node = entry.find('.//{*}Amt')
        credit = entry.find('./{*}CdtDbtInd')
        # NB: Elements without children are falsy - never chain with "or"
        date_node = entry.find('.//{*}BookgDt/{*}Dt')
        if date_node is None:
            date_node = entry.find('.//{*}ValDt/{*}Dt')
        if amount_node is None or date_node is None:
            continue
        amount = _to_float(amount_node.text, '.', ',')
        if credit is not None and credit.text == 'DBIT':
            amount = -amount
        try:
            entry_date = datetime.fromisoformat(
                date_node.text[:10]).date()
        except ValueError:
            continue
        comm_node = entry.find('.//{*}AddtlNtryInf')
        ref_node = entry.find('.//{*}AcctSvcrRef') or \
            entry.find('.//{*}EndToEndId')
        communication = ' '.join((comm_node.text or '').split()) \
            if comm_node is not None and comm_node.text else ''
        reference = (ref_node.text or '').strip() if ref_node is not None else ''
        lines.append({
            'date': entry_date,
            'amount': amount,
            'reference': reference or communication[:60],
            'communication': communication,
            'currency': amount_node.get('Ccy'),
        })
    if not lines:
        raise ParseError('No Ntry entries found in CAMT.053 file.')
    return {'lines': lines, 'balance_start': balance_start,
            'balance_end': balance_end, 'currency': currency}


# ----------------------------------------------------------------------
# OFX
# ----------------------------------------------------------------------
def parse_ofx(raw_bytes, **kwargs):
    text = raw_bytes.decode('utf-8', errors='replace')
    lines_out = []
    for block in re.findall(r'<STMTTRN>(.*?)</STMTTRN>', text, re.S | re.I):
        def field(name, default=''):
            m = re.search(r'<%s>([^<\r\n]+)' % name, block, re.I)
            return m.group(1).strip() if m else default
        raw_date = field('DTPOSTED')[:8]
        try:
            entry_date = datetime.strptime(raw_date, '%Y%m%d').date()
        except ValueError:
            continue
        lines_out.append({
            'date': entry_date,
            'amount': _to_float(field('TRNAMT'), '.', ','),
            'reference': field('FITID') or field('CHECKNUM'),
            'communication': ' '.join(
                (field('NAME') + ' ' + field('MEMO')).split()),
            'currency': False,
        })
    if not lines_out:
        raise ParseError('No STMTTRN transactions found in OFX file.')
    return {'lines': lines_out, 'balance_start': 0.0,
            'balance_end': 0.0, 'currency': False}


# ----------------------------------------------------------------------
# QIF
# ----------------------------------------------------------------------
def parse_qif(raw_bytes, **kwargs):
    text = raw_bytes.decode('utf-8', errors='replace')
    lines_out = []
    current = {'date': None, 'amount': 0.0, 'reference': '',
               'communication': ''}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('!Type'):
            current = {'date': None, 'amount': 0.0, 'reference': '',
                       'communication': ''}
        elif current is not None:
            if line.startswith('D'):
                try:
                    current['date'] = _parse_date(line[1:], '%d/%m/%Y')
                except ParseError:
                    current['date'] = _parse_date(line[1:], '%m/%d/%Y')
            elif line.startswith('T'):
                current['amount'] = _to_float(line[1:], '.', ',')
            elif line.startswith('P'):
                current['communication'] = line[1:]
                current['reference'] = line[1:60]
            elif line.startswith('^'):
                if current['date']:
                    lines_out.append(current)
                current = {'date': None, 'amount': 0.0, 'reference': '',
                           'communication': ''}
    if not lines_out:
        raise ParseError('No transactions found in QIF file.')
    return {'lines': lines_out, 'balance_start': 0.0,
            'balance_end': 0.0, 'currency': False}


# ----------------------------------------------------------------------
# CSV (template-driven)
# ----------------------------------------------------------------------
def parse_csv(raw_bytes, template=None, **kwargs):
    if template is None:
        raise ParseError('CSV import requires a template.')
    encoding = template.csv_encoding or 'utf-8-sig'
    text = raw_bytes.decode(encoding, errors='replace')
    delimiter = template.csv_delimiter or ';'
    reader = csv_module.reader(StringIO(text), delimiter=delimiter)
    rows = list(reader)

    start = max(0, template.csv_header_row or 0)
    rows = rows[start:]
    if not rows:
        raise ParseError('CSV file is empty.')

    lines = []
    for row in rows:
        if not any(cell.strip() for cell in row):
            continue

        def cell(idx):
            if idx is None or idx < 0 or idx >= len(row):
                return ''
            return row[idx].strip()

        try:
            entry_date = _parse_date(cell(template.date_col),
                                     template.date_format)
        except ParseError:
            continue
        amount = _to_float(cell(template.amount_col),
                           template.decimal_separator,
                           template.thousands_separator or '')
        dc_marker = cell(template.debit_credit_col).upper()
        if template.debit_credit_col >= 0 and dc_marker:
            if dc_marker.startswith(template.debit_value or 'D'):
                amount = -abs(amount)
            else:
                amount = abs(amount)
        elif amount > 0 and template.debit_credit_col >= 0:
            amount = -amount
        value_date = cell(template.value_date_col)
        lines.append({
            'date': entry_date,
            'amount': amount,
            'reference': cell(template.reference_col) or entry_date.isoformat(),
            'communication': cell(template.communication_col)
            or cell(template.partner_col),
            'partner_name': cell(template.partner_col),
            'currency': cell(template.currency_col) or False,
        })
    if not lines:
        raise ParseError('No data rows could be parsed from CSV. '
                         'Check the template column mapping.')
    return {'lines': lines, 'balance_start': 0.0,
            'balance_end': 0.0, 'currency': False}


PARSERS = {
    'mt940': parse_mt940,
    'camt053': parse_camt053,
    'ofx': parse_ofx,
    'qif': parse_qif,
    'csv': parse_csv,
}


def run_parser(template, raw_bytes):
    parser = PARSERS.get(template.file_format)
    if not parser:
        raise ParseError('Unknown format: %s' % template.file_format)
    return parser(raw_bytes, template=template)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.bank.stmt.run'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
