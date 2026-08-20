# -*- coding: utf-8 -*-
from odoo import fields, models


class ItAssetHrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_it_asset_ids = fields.One2many('sf.it.asset', 'assignee_id',
                                      string='IT Assets')