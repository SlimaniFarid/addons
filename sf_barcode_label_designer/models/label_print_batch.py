# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LabelPrintBatch(models.Model):
    _name = 'sf.barcode.label.designer.label.print.batch'
    _description = 'Label Print Batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    template_id = fields.Many2one(required=True, comodel_name='sf.barcode.label.designer.label.template', ondelete='restrict')
    quantity = fields.Integer(string='Quantity', default=1)
    model_ref = fields.Reference(string='Model Ref')
    state = fields.Selection([
        ('draft', 'Draft'), ('queued', 'Queued'), ('printing', 'Printing'),
        ('printed', 'Printed'), ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', copy=False)

