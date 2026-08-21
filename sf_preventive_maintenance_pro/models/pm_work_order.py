# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PmWorkOrder(models.Model):
    _name = 'sf.preventive.maintenance.pro.pm.work.order'
    _description = 'Pm Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.Many2one(comodel_name='pm.plan', ondelete='restrict')
    maintenance_request_id = fields.Many2one(comodel_name='maintenance.request', ondelete='restrict')
    created_date = fields.Date(string='Created Date', default=fields.Date.today)
    state = fields.Selection(default='pending')

