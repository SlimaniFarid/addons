from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QMSNonConformity(models.Model):
    _name = 'qms.nc'
    _description = 'Non-Conformity (NC)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='NC Number', required=True, copy=False, default='New')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    # Source
    source = fields.Selection([
        ('internal_audit', 'Internal Audit'),
        ('external_audit', 'External Audit'),
        ('customer_complaint', 'Customer Complaint'),
        ('supplier', 'Supplier Issue'),
        ('production', 'Production Defect'),
        ('inspection', 'Inspection Failure'),
        ('other', 'Other'),
    ], string='Source', required=True)

    # Details
    description = fields.Html(string='Description', required=True)
    detected_date = fields.Date(string='Detected Date', default=fields.Date.today)
    detected_by_id = fields.Many2one('res.users', string='Detected By', default=lambda s: s.env.user)
    location_id = fields.Many2one('stock.location', string='Location')
    product_id = fields.Many2one('product.product', string='Product')
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial')

    # Classification
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', required=True, default='minor')

    iso_clause = fields.Char(string='ISO Clause Reference')
    requirement = fields.Text(string='Requirement Not Met')

    # Status
    state = fields.Selection([
        ('open', 'Open'),
        ('containment', 'Containment'),
        ('analysis', 'Root Cause Analysis'),
        ('capa', 'CAPA Defined'),
        ('implementation', 'Implementation'),
        ('verification', 'Effectiveness Verification'),
        ('closed', 'Closed'),
    ], string='Status', default='open', tracking=True)

    # Containment
    containment_action = fields.Html(string='Containment Action')
    containment_by_id = fields.Many2one('res.users', string='Containment By')
    containment_date = fields.Date(string='Containment Date')
    containment_verified = fields.Boolean(string='Containment Verified')

    # Root Cause
    root_cause = fields.Html(string='Root Cause Analysis')
    root_cause_method = fields.Selection([
        ('5whys', '5 Whys'),
        ('fishbone', 'Fishbone / Ishikawa'),
        ('pareto', 'Pareto Analysis'),
        ('fault_tree', 'Fault Tree Analysis'),
        ('other', 'Other'),
    ], string='Analysis Method')
    root_cause_by_id = fields.Many2one('res.users', string='Analyzed By')
    root_cause_date = fields.Date(string='Analysis Date')

    # CAPA Link
    capa_id = fields.Many2one('qms.capa', string='Linked CAPA', readonly=True)

    # Closure
    closure_notes = fields.Text(string='Closure Notes')
    closed_by_id = fields.Many2one('res.users', string='Closed By')
    closed_date = fields.Date(string='Closed Date')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qms.nc') or 'NC-%s' % self.env['ir.sequence'].next_by_code('qms.nc')
        return super().create(vals_list)

    def action_containment(self):
        self.write({'state': 'containment'})

    def action_analysis(self):
        self.write({'state': 'analysis'})

    def action_create_capa(self):
        capa = self.env['qms.capa'].create({
            'nc_id': self.id,
            'title': f'CAPA for {self.name}',
            'description': self.description,
        })
        self.write({'state': 'capa', 'capa_id': capa.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qms.capa',
            'res_id': capa.id,
            'view_mode': 'form',
        }

    def action_verify_effectiveness(self):
        self.write({'state': 'verification'})

    def action_close(self):
        self.write({'state': 'closed', 'closed_by_id': self.env.user.id, 'closed_date': fields.Date.today()})


class QMSNCAttachment(models.Model):
    _name = 'qms.nc.attachment'
    _description = 'NC Attachment'

    nc_id = fields.Many2one('qms.nc', string='Non-Conformity', required=True, ondelete='cascade')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', required=True)
    description = fields.Char(string='Description')