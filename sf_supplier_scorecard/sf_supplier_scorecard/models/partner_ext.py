# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PartnerScorecard(models.Model):
    _inherit = 'res.partner'

    sf_scorecard_ids = fields.One2many('sf.supplier.scorecard',
                                       'partner_id',
                                       string='Scorecards')