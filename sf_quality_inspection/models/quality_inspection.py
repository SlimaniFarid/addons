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

    plan_id = fields.Many2one('sf.quality_inspection.inspection.plan', string='Plan Id', required=True)
    picking_id = fields.Many2one('stock.picking', string='Picking Id')
    result = fields.Selection([('pass','Pass'),('fail','Fail'),('pending','Pending')], string='Result', default='pending tracking', tracking=True)
    inspector_id = fields.Many2one('res.users', string='Inspector Id', default='current')
    notes = fields.Html(string='Notes')
    photo_ids = fields.Many2many('ir.attachment', string='Photo Ids')

