from odoo import api, fields, models


class PortalDocument(models.Model):
    _name = 'portal.document'
    _description = 'Portal Document'
    _order = 'create_date desc'

    config_id = fields.Many2one('portal.config', string='Portal Config', required=True, ondelete='cascade')
    name = fields.Char(string='Document Name', required=True)
    description = fields.Text(string='Description')
    document_type = fields.Selection([
        ('contract', 'Contract'),
        ('certificate', 'Certificate'),
        ('compliance', 'Compliance Document'),
        ('invoice', 'Invoice'),
        ('statement', 'Account Statement'),
        ('report', 'Report'),
        ('other', 'Other'),
    ], string='Type', required=True)

    file = fields.Binary(string='File', attachment=True, required=True)
    filename = fields.Char(string='Filename')
    mimetype = fields.Char(string='MIME Type')

    # Access control
    partner_ids = fields.Many2many('res.partner', string='Visible To Partners',
        help='Empty = all portal users of the company')
    company_ids = fields.Many2many('res.company', string='Companies')

    # Visibility
    active = fields.Boolean(default=True)
    publish_date = fields.Date(string='Publish Date')
    expiry_date = fields.Date(string='Expiry Date')
    is_featured = fields.Boolean(string='Featured')

    # Metadata
    tags = fields.Many2many('portal.document.tag', string='Tags')
    version = fields.Char(string='Version', default='1.0')
    version_notes = fields.Text(string='Version Notes')

    def action_download(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/file/{self.filename}',
            'target': 'self',
        }


class PortalDocumentTag(models.Model):
    _name = 'portal.document.tag'
    _description = 'Portal Document Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')