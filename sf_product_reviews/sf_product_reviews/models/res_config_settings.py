# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_product_reviews_moderation_required = fields.Boolean(
        string='Moderation Required',
        default=True,
        config_parameter='sf_product_reviews.moderation_required',
    )
    sf_product_reviews_approval_threshold = fields.Integer(
        string='Approval Threshold (rating)',
        default=4,
        config_parameter='sf_product_reviews.approval_threshold',
    )