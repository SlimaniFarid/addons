# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ScheduleSlot(models.Model):
    _name = 'sf.production.scheduling.schedule.slot'
    _description = 'Schedule Slot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.Many2one(required=True, comodel_name='sf.production.scheduling.schedule.plan', ondelete='restrict')
    mo_id = fields.Many2one(comodel_name='mrp.production', ondelete='restrict')
    start_datetime = fields.Datetime(string='Start Datetime')
    end_datetime = fields.Datetime(string='End Datetime')
    workcenter_id = fields.Many2one(comodel_name='mrp.workcenter', ondelete='restrict')

