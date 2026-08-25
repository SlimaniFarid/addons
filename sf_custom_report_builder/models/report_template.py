import base64
import json
import logging
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


BLOCK_TYPES = [
    ('logo', 'Logo'),
    ('text', 'Rich Text'),
    ('field', 'Dynamic Field'),
    ('table', 'Line Table'),
    ('signature', 'Signature'),
    ('separator', 'Separator'),
    ('spacer', 'Spacer'),
    ('image', 'Static Image'),
    ('html', 'Raw HTML'),
    ('pagebreak', 'Page Break'),
]


class ReportTemplate(models.Model):
    _name = 'report.template'
    _description = 'Custom PDF Report Template'
    _order = 'sequence, name'

    name = fields.Char(string='Template Name', required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    model_id = fields.Many2one('ir.model', string='Applicable Model', required=True)
    report_name = fields.Char(string='Report Name (QWeb)', required=True)
    description = fields.Text(string='Description')

    # Page settings
    paper_format_id = fields.Many2one('report.paperformat', string='Paper Format')
    margin_top = fields.Integer(string='Margin Top (mm)', default=20)
    margin_bottom = fields.Integer(string='Margin Bottom (mm)', default=20)
    margin_left = fields.Integer(string='Margin Left (mm)', default=15)
    margin_right = fields.Integer(string='Margin Right (mm)', default=15)
    orientation = fields.Selection([
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ], string='Orientation', default='portrait')

    # Header/Footer
    header_html = fields.Html(string='Header HTML')
    footer_html = fields.Html(string='Footer HTML')
    show_page_numbers = fields.Boolean(string='Page Numbers', default=True)

    block_ids = fields.One2many('report.block', 'template_id', string='Blocks')
    assignment_ids = fields.One2many('report.assignment', 'template_id', string='Assignments')

    def action_preview(self):
        self.ensure_one()
        # Generate preview with a sample record
        Model = self.env[self.model_id.model]
        sample = Model.search([], limit=1)
        if not sample:
            raise UserError('No sample record found for model %s' % self.model_id.model)
        return self._render_report(sample)

    def _render_report(self, record):
        self.ensure_one()
        qweb_content = self._build_qweb()
        report = self.env['ir.actions.report']._get_report_from_name(self.report_name)
        if not report:
            # Create report action
            report = self.env['ir.actions.report'].create({
                'name': self.name,
                'model': self.model_id.model,
                'report_name': self.report_name,
                'report_type': 'qweb-pdf',
                'paperformat_id': self.paper_format_id.id,
            })
        # Render using the generated QWeb
        pdf, _ = report._render_qweb_pdf(record.ids)
        return pdf

    def _build_qweb(self):
        self.ensure_one()
        blocks_html = []
        for block in self.block_ids.sorted('sequence'):
            blocks_html.append(block.to_qweb())
        header = self.header_html or ''
        footer = self.footer_html or ''
        if self.show_page_numbers:
            footer += '<div class="text-center text-muted" style="font-size: 8pt;">Page <span class="page"></span> / <span class="topage"></span></div>'

        qweb = f"""
        <t t-name="{self.report_name}">
            <div class="container">
                {header}
                {''.join(blocks_html)}
                {footer}
            </div>
        </t>
        """
        return qweb


class ReportBlock(models.Model):
    _name = 'report.block'
    _description = 'Report Template Block'
    _order = 'sequence'

    template_id = fields.Many2one('report.template', string='Template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    block_type = fields.Selection(BLOCK_TYPES, string='Type', required=True)
    name = fields.Char(string='Block Name')

    # Text block
    text_content = fields.Html(string='Content')

    # Field block
    field_name = fields.Char(string='Field Name', help='Dot notation: partner_id.name')
    field_label = fields.Char(string='Label')
    field_format = fields.Selection([
        ('raw', 'Raw'),
        ('currency', 'Currency'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('float', 'Float (2 decimals)'),
        ('percentage', 'Percentage'),
    ], string='Format', default='raw')

    # Table block
    table_model = fields.Char(string='Sub-model', help='e.g., order_line')
    table_fields = fields.Text(string='Fields (JSON)', help='[{"name": "product_id", "label": "Product"}, {"name": "price_unit", "label": "Price"}]')
    table_header_color = fields.Char(string='Header Color', default='#343a40')

    # Signature block
    signature_field = fields.Char(string='Signature Field', help='Field containing signature image (base64)')
    signature_label = fields.Char(string='Label', default='Signature')

    # Image block
    image_field = fields.Char(string='Image Field', help='Field containing image (base64 or binary)')
    image_width = fields.Integer(string='Width (mm)', default=50)
    image_height = fields.Integer(string='Height (mm)', default=50)

    # Style
    css_class = fields.Char(string='CSS Classes')
    style = fields.Text(string='Inline Styles')
    condition = fields.Char(string='Condition', help='Python expression on record, e.g., "record.state == \"sale\""')

    def to_qweb(self):
        self.ensure_one()
        cond = f' t-if="{self.condition}"' if self.condition else ''
        cls = f' class="{self.css_class}"' if self.css_class else ''
        style = f' style="{self.style}"' if self.style else ''

        if self.block_type == 'logo':
            return f'<div{cls}{style}{cond}><img t-att-src="record.company_id.logo" style="max-height: 60px;"/></div>'
        elif self.block_type == 'text':
            return f'<div{cls}{style}{cond}>{self.text_content or ""}</div>'
        elif self.block_type == 'field':
            label = f'<strong>{self.field_label}:</strong> ' if self.field_label else ''
            fmt = self.field_format
            if fmt == 'currency':
                expr = f"formatLang(record.{self.field_name}, currency_obj=record.currency_id)"
            elif fmt == 'date':
                expr = f"format_date(env, record.{self.field_name})"
            elif fmt == 'datetime':
                expr = f"format_datetime(env, record.{self.field_name})"
            elif fmt == 'float':
                expr = f"'%.2f' % record.{self.field_name}"
            elif fmt == 'percentage':
                expr = f"'%.1f%%' % (record.{self.field_name} * 100)"
            else:
                expr = f"record.{self.field_name}"
            return f'<div{cls}{style}{cond}>{label}<span t-esc="{expr}"/></div>'
        elif self.block_type == 'table':
            return self._build_table_qweb(cond, cls, style)
        elif self.block_type == 'signature':
            return f'<div{cls}{style}{cond} t-if="record.{self.signature_field}"><p>{self.signature_label}</p><img t-att-src="\'data:image/png;base64,\' + record.{self.signature_field}" style="max-width: 200px;"/></div>'
        elif self.block_type == 'separator':
            return f'<hr{cls}{style}{cond}/>'
        elif self.block_type == 'spacer':
            return f'<div{cls}{style}{cond} style="height: 20px;"/></div>'
        elif self.block_type == 'image':
            return f'<div{cls}{style}{cond} t-if="record.{self.image_field}"><img t-att-src="\'data:image/png;base64,\' + record.{self.image_field}" style="width: {self.image_width}mm; height: {self.image_height}mm;"/></div>'
        elif self.block_type == 'html':
            return f'<div{cls}{style}{cond} t-raw="record.{self.field_name}"/>'
        elif self.block_type == 'pagebreak':
            return f'<div{cls}{style}{cond} style="page-break-after: always;"/></div>'
        return f'<div{cls}{style}{cond}>[Unknown block: {self.block_type}]</div>'

    def _build_table_qweb(self, cond, cls, style):
        try:
            fields = json.loads(self.table_fields or '[]')
        except Exception:
            fields = []
        if not fields:
            return f'<div{cls}{style}{cond} t-if="record.{self.table_model}"><table class="table table-sm"><thead><tr><th>No data</th></tr></thead><tbody><tr t-foreach="record.{self.table_model}" t-as="line"><td><span t-esc="line.display_name"/></td></tr></tbody></table></div>'

        header = ''.join(f'<th style="background: {self.table_header_color}; color: white; padding: 4px;">{f.get("label", f.get("name"))}</th>' for f in fields)
        rows = ''
        for f in fields:
            name = f.get('name')
            fmt = f.get('format', 'raw')
            if fmt == 'currency':
                cell = f'formatLang(line.{name}, currency_obj=line.currency_id)'
            elif fmt == 'float':
                cell = f"'%.2f' % line.{name}"
            else:
                cell = f'line.{name}'
            rows += f'<td style="padding: 4px;"><span t-esc="{cell}"/></td>'

        return f'''
        <div{cls}{style}{cond} t-if="record.{self.table_model}">
            <table class="table table-sm table-bordered">
                <thead><tr>{header}</tr></thead>
                <tbody>
                    <tr t-foreach="record.{self.table_model}" t-as="line">
                        {rows}
                    </tr>
                </tbody>
            </table>
        </div>
        '''


class ReportAssignment(models.Model):
    _name = 'report.assignment'
    _description = 'Report Template Assignment'
    _order = 'sequence'

    template_id = fields.Many2one('report.template', string='Template', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one('res.company', string='Company',
        help='Empty = all companies')
    report_action_id = fields.Many2one('ir.actions.report', string='Standard Report',
        help='Replace this standard report with the custom template')
    condition = fields.Char(string='Condition', help='Python expression on record')

    def applies_to(self, record):
        self.ensure_one()
        if self.company_id and record.company_id != self.company_id:
            return False
        if self.condition:
            try:
                return bool(safe_eval(self.condition, {'record': record}, mode="eval", nocopy=True))
            except Exception:
                return False
        return True