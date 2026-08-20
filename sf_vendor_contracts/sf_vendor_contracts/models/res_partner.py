# -*- coding: utf-8 -*-
from odoo import fields, models


class VendorContractResPartner(models.Model):
    _inherit = 'res.partner'

    sf_vendor_contract_ids = fields.One2many('sf.vendor.contract',
                                             'partner_id',
                                             string='Contracts')