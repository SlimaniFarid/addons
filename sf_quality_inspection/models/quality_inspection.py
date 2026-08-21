# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class QualityInspection(models.Model):
    _name = 'sf.quality.inspection.quality.inspection'
    _description = 'Quality Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.Many2one(required=True, comodel_name='inspection.plan', ondelete='restrict')
    picking_id = fields.Many2one(comodel_name='stock.picking', ondelete='restrict')
    result = fields.Selection(default='pending tracking', tracking=True)
    inspector_id = fields.Many2one(default='current', comodel_name='res.users', ondelete='restrict')
    notes = fields.Html(string='Notes')
    photo_ids = fields.Many2many('ir.attachment', string='Photo Ids')

