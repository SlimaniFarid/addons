from odoo import api, fields, models


class EDIDocument(models.Model):
    _name = 'edi.document'
    _description = 'EDI Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Document Reference', required=True, copy=False, default='New')
    partner_id = fields.Many2one('edi.partner', string='Trading Partner', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    direction = fields.Selection([
        ('inbound', 'Inbound (Received)'),
        ('outbound', 'Outbound (Sent)'),
    ], string='Direction', required=True)

    document_type_id = fields.Many2one('edi.document.type', string='Document Type', required=True)
    format_id = fields.Many2one('edi.format', string='Format', required=True)

    # Source/Target
    source_record = fields.Reference(
        selection='_selection_source_models',
        string='Source Record',
        help='Odoo record that generated this document'
    )
    source_record_id = fields.Integer(string='Source Record ID')

    # Content
    raw_content = fields.Binary(string='Raw Content (XML/JSON)', attachment=True)
    raw_filename = fields.Char(string='Raw Filename')
    parsed_data = fields.Text(string='Parsed Data (JSON)')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validating', 'Validating'),
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
        ('transmitting', 'Transmitting'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True)

    # Transmission
    transmission_ids = fields.One2many('edi.transmission', 'document_id', string='Transmissions')
    validation_errors = fields.Text(string='Validation Errors')

    # Peppol specific
    peppol_message_id = fields.Char(string='Peppol Message ID')
    peppol_status = fields.Selection([
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ], string='Peppol Status')

    @api.model
    def _selection_source_models(self):
        return [
            ('account.move', 'Invoice/Bill'),
            ('sale.order', 'Sale Order'),
            ('purchase.order', 'Purchase Order'),
            ('stock.picking', 'Delivery/Receipt'),
        ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('edi.document') or 'EDI-%s' % self.env['ir.sequence'].next_by_code('edi.document')
        return super().create(vals_list)

    def action_validate(self):
        for doc in self:
            doc.state = 'validating'
            # Validate against schema/schematron
            errors = doc._validate_against_schema()
            if errors:
                doc.write({'state': 'invalid', 'validation_errors': '\n'.join(errors)})
            else:
                doc.write({'state': 'valid'})

    def _validate_against_schema(self):
        # Simplified validation
        return []

    def action_transmit(self):
        for doc in self.filtered(lambda d: d.state == 'valid'):
            doc.state = 'transmitting'
            transmission = self.env['edi.transmission'].create({
                'document_id': doc.id,
                'partner_id': doc.partner_id.id,
                'direction': doc.direction,
            })
            transmission.action_send()