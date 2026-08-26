# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    sf_staffing_mission_id = fields.Many2one('sf.staffing.mission', string='Staffing Mission', ondelete='set null', index=True)