from odoo import api, fields, models


class EDIDocumentType(models.Model):
    _name = 'edi.document.type'
    _description = 'EDI Document Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    standard = fields.Selection([
        ('ubl', 'UBL 2.1'),
        ('cii', 'CII'),
        ('facturx', 'Factur-X'),
        ('x12', 'ANSI X12'),
        ('cfdi', 'CFDI 4.0'),
        ('ksef', 'KSeF'),
        ('fatturapa', 'FatturaPA'),
    ], string='Standard', required=True)
    direction = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('both', 'Both'),
    ], string='Direction', default='both')
    description = fields.Text(string='Description')


class EDIFormat(models.Model):
    _name = 'edi.format'
    _description = 'EDI Format'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    standard = fields.Selection([
        ('ubl', 'UBL 2.1'),
        ('cii', 'CII'),
        ('facturx', 'Factur-X'),
        ('x12', 'ANSI X12'),
        ('cfdi', 'CFDI 4.0'),
        ('ksef', 'KSeF'),
        ('fatturapa', 'FatturaPA'),
    ], string='Standard', required=True)
    version = fields.Char(string='Version', default='1.0')
    schema_url = fields.Char(string='Schema URL')
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')