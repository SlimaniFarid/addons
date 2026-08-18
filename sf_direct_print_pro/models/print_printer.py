import socket
import logging
import base64
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PrintPrinter(models.Model):
    _name = 'print.printer'
    _description = 'Network Printer'
    _order = 'name'

    name = fields.Char(string='Printer Name', required=True)
    printer_type = fields.Selection([
        ('network', 'Network (TCP/IP)'),
        ('usb', 'USB (via PrintNode)'),
        ('bluetooth', 'Bluetooth'),
        ('cloud', 'Cloud (PrintNode)'),
    ], string='Connection Type', required=True, default='network')
    active = fields.Boolean(default=True)

    # Network settings
    host = fields.Char(string='Host / IP Address', help='IP address or hostname of the printer')
    port = fields.Integer(string='Port', default=9100, help='Default 9100 for raw TCP printing')
    timeout = fields.Integer(string='Timeout (seconds)', default=5)

    # PrintNode settings
    printnode_printer_id = fields.Integer(string='PrintNode Printer ID')
    printnode_api_key = fields.Char(string='PrintNode API Key', groups='base.group_system')

    # Capabilities
    supports_zpl = fields.Boolean(string='Supports ZPL', default=True)
    supports_pdf = fields.Boolean(string='Supports PDF', default=False)
    supports_raw = fields.Boolean(string='Supports Raw', default=True)
    paper_width_mm = fields.Integer(string='Paper Width (mm)', default=102)
    paper_height_mm = fields.Integer(string='Paper Height (mm)', default=152)

    profile_ids = fields.One2many('print.profile', 'printer_id', string='Profiles')
    job_ids = fields.One2many('print.job', 'printer_id', string='Print Jobs')

    def test_connection(self):
        self.ensure_one()
        if self.printer_type == 'network':
            try:
                sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
                sock.close()
                return {'type': 'ir.actions.client', 'tag': 'display_notification',
                        'params': {'title': 'Success', 'message': 'Printer reachable', 'type': 'success'}}
            except Exception as e:
                raise UserError(f'Connection failed: {e}')
        elif self.printer_type == 'cloud':
            if not self.printnode_printer_id or not self.printnode_api_key:
                raise UserError('PrintNode credentials missing')
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Info', 'message': 'PrintNode config present', 'type': 'info'}}
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': 'Info', 'message': 'Test not implemented for this type', 'type': 'info'}}

    def send_raw(self, data):
        self.ensure_one()
        if self.printer_type != 'network':
            raise UserError('Direct TCP printing only for network printers')
        try:
            sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            sock.sendall(data)
            sock.close()
            return True
        except Exception as e:
            _logger.exception('Print failed')
            raise UserError(f'Print failed: {e}')

    def send_pdf(self, pdf_data):
        self.ensure_one()
        if self.printer_type == 'cloud':
            # Would use PrintNode API
            raise UserError('Cloud printing via PrintNode not implemented in demo')
        raise UserError('PDF printing requires PrintNode or CUPS')


class PrintProfile(models.Model):
    _name = 'print.profile'
    _description = 'Print Profile'
    _order = 'sequence'

    name = fields.Char(string='Profile Name', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    printer_id = fields.Many2one('print.printer', string='Printer', required=True, ondelete='cascade')
    report_id = fields.Many2one('ir.actions.report', string='Report', required=True)
    model_id = fields.Many2one(related='report_id.model_id', store=True, readonly=True)

    format = fields.Selection([
        ('zpl', 'ZPL (Labels)'),
        ('pdf', 'PDF'),
        ('raw', 'Raw Text'),
    ], string='Format', default='zpl', required=True)

    copies = fields.Integer(string='Copies', default=1)
    auto_print = fields.Boolean(string='Auto Print on Event', default=False)
    trigger_model = fields.Char(string='Trigger Model', help='Model that triggers auto-print (e.g., stock.picking)')
    trigger_field = fields.Char(string='Trigger Field', help='Field to watch (e.g., state)')
    trigger_value = fields.Char(string='Trigger Value', help='Value that triggers print (e.g., done)')

    @api.onchange('report_id')
    def _onchange_report_id(self):
        if self.report_id:
            self.model_id = self.report_id.model_id

    def generate_content(self, record):
        self.ensure_one()
        if not self.report_id:
            return False
        report_sudo = self.report_id.sudo()
        if self.format == 'pdf':
            content, _ = report_sudo._render_qweb_pdf(record.ids)
            return content
        elif self.format == 'zpl':
            # ZPL generation would need a custom QWeb template or external tool
            content, _ = report_sudo._render_qweb_text(record.ids)
            return content.encode()
        return False


class PrintJob(models.Model):
    _name = 'print.job'
    _description = 'Print Job'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    printer_id = fields.Many2one('print.printer', string='Printer', required=True, ondelete='cascade')
    profile_id = fields.Many2one('print.profile', string='Profile', ondelete='set null')

    model = fields.Char(string='Model')
    res_id = fields.Integer(string='Record ID')
    format = fields.Selection([
        ('zpl', 'ZPL'),
        ('pdf', 'PDF'),
        ('raw', 'Raw'),
    ], string='Format', required=True)
    content = fields.Binary(string='Content', attachment=True)
    copies = fields.Integer(string='Copies', default=1)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('printing', 'Printing'),
        ('done', 'Done'),
        ('error', 'Error'),
    ], string='Status', default='draft', tracking=True)
    error_message = fields.Text(string='Error')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('print.job') or 'PRJ-%s' % self.env['ir.sequence'].next_by_code('print.job')
        return super().create(vals_list)

    def action_print(self):
        for job in self:
            if job.state in ('done', 'printing'):
                continue
            job.state = 'printing'
            try:
                data = base64.b64decode(job.content) if job.content else b''
                if job.format == 'zpl' and job.printer_id.supports_zpl:
                    job.printer_id.send_raw(data)
                elif job.format == 'pdf' and job.printer_id.supports_pdf:
                    job.printer_id.send_pdf(data)
                else:
                    job.printer_id.send_raw(data)
                job.state = 'done'
            except Exception as e:
                job.state = 'error'
                job.error_message = str(e)

    def action_retry(self):
        self.filtered(lambda j: j.state == 'error').write({'state': 'draft'}).action_print()