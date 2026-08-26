# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ExportIncoterm(models.Model):
    _name = 'sf.export.incoterm'
    _description = 'Export Incoterm'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code)',
         _('This Incoterm code already exists.')),
    ]


class ExportDossier(models.Model):
    _name = 'sf.export.dossier'
    _description = 'Export Dossier'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale order',
                                    ondelete='restrict', index=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True,
                                 ondelete='restrict', index=True)
    destination_country_id = fields.Many2one('res.country',
                                             string='Destination country',
                                             required=True)
    origin_country_id = fields.Many2one('res.country',
                                        string='Country of origin',
                                        required=True)
    incoterm_id = fields.Many2one('sf.export.incoterm', string='Incoterm')
    port_loading = fields.Char(string='Port of loading')
    port_discharge = fields.Char(string='Port of discharge')
    transport_mode = fields.Selection([
        ('sea', 'Sea'),
        ('air', 'Air'),
        ('road', 'Road'),
        ('rail', 'Rail'),
    ], string='Transport mode', default='sea', required=True)
    shipment_date = fields.Date(string='Shipment date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_preparation', 'In Preparation'),
        ('ready', 'Ready'),
        ('shipped', 'Shipped'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    doc_invoice_ok = fields.Boolean(string='Commercial invoice')
    doc_packing_ok = fields.Boolean(string='Packing list')
    doc_origin_ok = fields.Boolean(string='Certificate of origin')
    doc_eur_ok = fields.Boolean(string='EUR.1 / ATR')
    completeness = fields.Integer(string='Documents (0-4)',
                                  compute='_compute_completeness',
                                  store=True)
    shipped_date = fields.Datetime(string='Shipped on')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         _('This dossier number already exists.')),
    ]

    @api.depends('doc_invoice_ok', 'doc_packing_ok', 'doc_origin_ok',
                 'doc_eur_ok')
    def _compute_completeness(self):
        for dossier in self:
            dossier.completeness = sum([
                dossier.doc_invoice_ok,
                dossier.doc_packing_ok,
                dossier.doc_origin_ok,
                dossier.doc_eur_ok,
            ])

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.export.dossier')
            vals['name'] = 'EXP-%s' % seq
        if not vals.get('origin_country_id'):
            origin = self.env.company.sf_export_origin_country_id
            if origin:
                vals['origin_country_id'] = origin.id
        return super().create(vals)

    def action_start_preparation(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft dossiers can be put in '
                              'preparation.'))
        self.state = 'in_preparation'

    def action_mark_ready(self):
        self.ensure_one()
        if self.state != 'in_preparation':
            raise UserError(_('Only dossiers in preparation can be marked '
                              'as ready.'))
        if self.completeness < 4:
            raise UserError(_('The export pack is incomplete: %s of 4 '
                              'documents are present. Generate all '
                              'documents before marking the dossier ready.')
                            % (self.completeness,))
        self.state = 'ready'

    def action_mark_shipped(self):
        self.ensure_one()
        if self.state != 'ready':
            raise UserError(_('Only ready dossiers can be marked as '
                              'shipped.'))
        self.write({
            'state': 'shipped',
            'shipped_date': fields.Datetime.now(),
        })

    def action_archive(self):
        self.ensure_one()
        if self.state != 'shipped':
            raise UserError(_('Only shipped dossiers can be archived.'))
        self.state = 'archived'

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ('draft', 'in_preparation'):
            raise UserError(_('Only draft or in-preparation dossiers can '
                              'be cancelled.'))
        self.state = 'cancelled'

    def unlink(self):
        for dossier in self:
            if dossier.state not in ('draft', 'cancelled'):
                raise UserError(_('A dossier that is not a draft cannot be '
                                  'deleted.'))
        return super().unlink()

    def _check_in_preparation_overdue(self):
        today = fields.Date.today()
        dossiers = self.search([('state', '=', 'in_preparation')])
        for dossier in dossiers:
            limit = today - dossier.company_id.sf_export_alert_days
            if dossier.create_date.date() <= limit:
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Export dossier %s still in preparation')
                    % (dossier.name,),
                    user_id=self.env.user.id)