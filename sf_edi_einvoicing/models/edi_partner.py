from odoo import api, fields, models


class EDIPartner(models.Model):
    _name = 'edi.partner'
    _description = 'EDI Trading Partner'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string='Odoo Partner', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    gln = fields.Char(string='GLN (Global Location Number)', help='13-digit GS1 identifier')
    peppol_id = fields.Char(string='Peppol Participant ID', help='ISO 6523 identifier (e.g., 0192:123456789)')
    edi_code = fields.Char(string='EDI Code', help='Partner-specific EDI code (e.g., ANSI X12 ISA06)')

    supports_peppol = fields.Boolean(string='Peppol Enabled', default=True)
    supports_as2 = fields.Boolean(string='AS2 Enabled', default=False)
    supports_sftp = fields.Boolean(string='SFTP Enabled', default=False)
    supports_api = fields.Boolean(string='API Enabled', default=False)

    preferred_format = fields.Selection([
        ('ubl', 'UBL 2.1'),
        ('cii', 'UN/CEFACT CII'),
        ('facturx', 'Factur-X'),
        ('x12', 'ANSI X12'),
        ('cfdi', 'CFDI 4.0'),
        ('ksef', 'KSeF'),
        ('fatturapa', 'FatturaPA'),
    ], string='Preferred Format', default='ubl')

    peppol_smp_url = fields.Char(string='Peppol SMP URL')
    peppol_certificate = fields.Binary(string='Peppol Certificate', attachment=True)
    peppol_cert_expiry = fields.Date(string='Certificate Expiry')

    as2_url = fields.Char(string='AS2 URL')
    as2_cert = fields.Binary(string='AS2 Certificate', attachment=True)
    as2_encryption = fields.Selection([
        ('aes256', 'AES-256'),
        ('3des', '3DES'),
        ('rc2', 'RC2'),
    ], string='AS2 Encryption', default='aes256')

    sftp_host = fields.Char(string='SFTP Host')
    sftp_port = fields.Integer(string='SFTP Port', default=22)
    sftp_username = fields.Char(string='SFTP Username')
    sftp_password = fields.Char(string='SFTP Password', groups='base.group_system')
    sftp_key = fields.Binary(string='SSH Private Key', attachment=True, groups='base.group_system')

    supported_doc_types = fields.Many2many('edi.document.type', string='Supported Document Types')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ], string='Status', default='draft', tracking=True)

    last_exchange = fields.Datetime(string='Last Exchange', readonly=True)