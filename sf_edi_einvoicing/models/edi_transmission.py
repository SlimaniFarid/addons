from odoo import api, fields, models


class EDITransmission(models.Model):
    _name = 'edi.transmission'
    _description = 'EDI Transmission'
    _order = 'create_date desc'

    document_id = fields.Many2one('edi.document', string='Document', required=True, ondelete='cascade')
    partner_id = fields.Many2one('edi.partner', string='Partner', required=True)
    direction = fields.Selection([
        ('outbound', 'Outbound'),
        ('inbound', 'Inbound'),
    ], string='Direction', required=True)

    protocol = fields.Selection([
        ('peppol', 'Peppol'),
        ('as2', 'AS2'),
        ('sftp', 'SFTP'),
        ('api', 'REST API'),
        ('email', 'Email'),
    ], string='Protocol', required=True)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('retry', 'Retry Scheduled'),
    ], string='Status', default='pending', tracking=True)

    sent_at = fields.Datetime(string='Sent At')
    delivered_at = fields.Datetime(string='Delivered At')
    error_message = fields.Text(string='Error')
    retry_count = fields.Integer(string='Retry Count', default=0)
    max_retries = fields.Integer(string='Max Retries', default=3)

    response_data = fields.Text(string='Response (JSON)')

    def action_send(self):
        for tx in self:
            tx.state = 'sending'
            try:
                # Simulate sending based on protocol
                if tx.protocol == 'peppol':
                    tx._send_peppol()
                elif tx.protocol == 'as2':
                    tx._send_as2()
                elif tx.protocol == 'sftp':
                    tx._send_sftp()
                elif tx.protocol == 'api':
                    tx._send_api()
                tx.write({'state': 'sent', 'sent_at': fields.Datetime.now()})
            except Exception as e:
                _logger.exception('Transmission failed')
                tx.write({'state': 'failed', 'error_message': str(e)})
                if tx.retry_count < tx.max_retries:
                    tx.retry_count += 1
                    # Schedule retry

    def _send_peppol(self):
        self.write({'state': 'delivered', 'delivered_at': fields.Datetime.now()})

    def _send_as2(self):
        self.write({'state': 'delivered', 'delivered_at': fields.Datetime.now()})

    def _send_sftp(self):
        self.write({'state': 'delivered', 'delivered_at': fields.Datetime.now()})

    def _send_api(self):
        self.write({'state': 'delivered', 'delivered_at': fields.Datetime.now()})